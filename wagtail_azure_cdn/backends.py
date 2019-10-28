import importlib
import logging
from collections import defaultdict
from typing import Any, Dict, List, Mapping, Sequence
from urllib.parse import urlparse

from django.core.exceptions import ImproperlyConfigured

from wagtail.contrib.frontend_cache.backends import BaseBackend

logger = logging.getLogger("wagtail_azure_cdn")


class AzureCdnBackend(BaseBackend):
    def __init__(self, params: Mapping[str, Any]):
        if importlib.util.find_spec("azure.mgmt.cdn") is None:
            raise RuntimeError("Install azure-mgmt-cdn.")
        self._global_config = self._parse_config(params)
        self._sites_config = {}  # type: Dict[str, Any]
        sites = params.get("SITES", {})
        for hostname, site_config in sites.items():
            self._sites_config[hostname] = self._parse_config(site_config)

    def _parse_config(self, params: Mapping[str, Any]) -> Dict[str, Any]:
        new_config = {}
        settings_map = {
            "SUBSCRIPTION_ID": "subscription_id",
            "RESOURCE_GROUP_NAME": "resource_group_name",
            "CDN_PROFILE_NAME": "cdn_profile_name",
            "CDN_ENDPOINT_NAME": "cdn_endpoint_name",
            "CDN_SERVICE_URL": "cdn_service_url",
            "CREDENTIALS": "credentials",
        }
        for settings_key, internal_key in settings_map.items():
            try:
                new_config[internal_key] = params[settings_key]
            except KeyError:
                pass
        return new_config

    def _get_setting_for_hostname(
        self, hostname: str, setting: str, raise_exception: bool = True
    ) -> Any:
        try:
            return self._sites_config[hostname][setting]
        except KeyError:
            try:
                return self._global_config[setting]
            except KeyError:
                if raise_exception:
                    raise ImproperlyConfigured(
                        f"Missing Azure CDN front-end cache invalidator for "
                        f"setting: {setting} ({hostname})"
                    )

    def _filter_urls_by_hostname(self, urls: Sequence[str]) -> Dict[str, List[str]]:
        """
        Return a dict with hostname as its keys and list of paths as its values.
        """
        paths_by_host = defaultdict(list)  # type: Dict[str, List[str]]
        for url in urls:
            parse_result = urlparse(url)
            hostname = parse_result.hostname
            final_path = "/"
            if parse_result.path:
                final_path = parse_result.path
            if parse_result.params:
                final_path = f"{final_path};{parse_result.params}"
            if parse_result.query:
                final_path = f"{final_path}?{parse_result.query}"
            paths_by_host[hostname].append(final_path)
        return paths_by_host

    def _get_client_for_hostname(self, hostname: str):
        from azure.mgmt.cdn import CdnManagementClient

        azure_credentials = self._get_setting_for_hostname(hostname, "credentials")
        azure_subscription_id = self._get_setting_for_hostname(
            hostname, "subscription_id"
        )
        azure_cdn_service_url = self._get_setting_for_hostname(
            hostname, "cdn_service_url", raise_exception=False
        )
        return CdnManagementClient(
            credentials=azure_credentials()
            if callable(azure_credentials)
            else azure_credentials,
            subscription_id=azure_subscription_id,
            base_url=azure_cdn_service_url,
        )

    def _purge_content(self, hostname: str, paths: Sequence[str]) -> None:
        from msrest.exceptions import HttpOperationError

        client = self._get_client_for_hostname(hostname)
        azure_resource_group_name = self._get_setting_for_hostname(
            hostname, "resource_group_name"
        )
        azure_cdn_profile_name = self._get_setting_for_hostname(
            hostname, "cdn_profile_name"
        )
        azure_cdn_endpoint_name = self._get_setting_for_hostname(
            hostname, "cdn_endpoint_name"
        )
        try:
            client.endpoints.purge_content(
                resource_group_name=azure_resource_group_name,
                profile_name=azure_cdn_profile_name,
                endpoint_name=azure_cdn_endpoint_name,
                content_paths=paths,
            )
        except HttpOperationError:
            logger.exception("Error purging content from Azure CDN: %r.", paths)
            raise

    def purge_batch(self, urls: Sequence[str]) -> None:
        for hostname, paths in self._filter_urls_by_hostname(urls).items():
            self._purge_content(hostname, paths)

    def purge(self, url: str) -> None:
        self.purge_batch([url])
