import logging
from urllib.parse import urlparse

import requests

logger = logging.getLogger('wagtail_azure_cdn')

AZURE_URL = (
    "https://management.azure.com/subscriptions/{subscription_id}/"
    "resourceGroups/{resource_group_name}/providers/Microsoft.Cdn/"
    "profiles/{profile_name}/endpoints/{endpoint_name}/purge"
    "?api-version=2017-10-12"
)


class AzureCdnBackend(BaseBackend):
    def __init__(self, params):
        self.azure_subscription_id = params.pop('SUBSCRIPTION_ID')
        self.azure_resource_group_name = params.pop('RESOURCE_GROUP_NAME')
        self.azure_cdn_profile_name = params.pop('CDN_PROFILE_NAME')
        self.azure_cdn_endpoint_name = params.pop('CDN_ENDPOINT_NAME')
        self.azure_sas_token = params.pop('SAS_TOKEN')

    def _get_path(self, url):
        parse_result = urlparse(url)
        return parse_result.path

    def purge_batch(self, urls):
        try:
            purge_url = AZURE_URL.format({
                'subscription_id': self.azure_subscription_id
                'resource_group_name': self.azure_resource_group_name,
                'profile_name': self.azure_cdn_profile_name,
                'endpoint_name': self.azure_cdn_endpoint_name,
            })

            headers = {
                "Content-Type": "application/json",
                "Authorization": "SharedAccessSignature {sas_token}".format({
                    "sas_token": self.azure_sas_token
                }),
            }

            data = {"contentPaths": [self._get_path(url) for url in urls]}

            response = requests.post(
                purge_url,
                json=data,
                headers=headers,
            )
            response.raise_for_status()

            try:
                response_json = response.json()
            except ValueError:
                for url in urls:
                    logger.error("Couldn't purge '%s' from Azure CDN. Unexpected JSON parse error.", url)

        except requests.exceptions.HTTPError as e:
            for url in urls:
                logging.exception(
                    "Couldn't purge '%s' from Azure CDN. HTTPError: %d. Error detail: %r",
                    url,
                    e.response.status_code,
                    response_json
                )


    def purge(self, url):
        self.purge_batch([url])
