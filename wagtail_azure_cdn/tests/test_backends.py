from django import test
from django.core.exceptions import ImproperlyConfigured

from faker import Faker

from wagtail_azure_cdn.backends import AzureCdnBackend


class TestAzureCdnBackend(test.TestCase):
    def test_subscription_id_setting(self):
        backend = AzureCdnBackend({"SUBSCRIPTION_ID": "test-subscription-id"})
        self.assertEqual(
            backend._get_setting_for_hostname("torchbox.com", "subscription_id"),
            "test-subscription-id",
        )

    def test_resource_group_name(self):
        backend = AzureCdnBackend({"RESOURCE_GROUP_NAME": "some-resource"})
        self.assertEqual(
            backend._get_setting_for_hostname("torchbox.com", "resource_group_name"),
            "some-resource",
        )

    def test_cdn_profile_name(self):
        backend = AzureCdnBackend({"CDN_PROFILE_NAME": "test-profile-name"})
        self.assertEqual(
            backend._get_setting_for_hostname("torchbox.com", "cdn_profile_name"),
            "test-profile-name",
        )

    def test_cdn_service_url(self):
        backend = AzureCdnBackend({"CDN_SERVICE_URL": "https://torchbox.com"})
        self.assertEqual(
            backend._get_setting_for_hostname("torchbox.com", "cdn_service_url"),
            "https://torchbox.com",
        )

    def test_multi_site(self):
        backend = AzureCdnBackend(
            {
                "RESOURCE_GROUP_NAME": "oxfam-production",
                "SUBSCRIPTION_ID": "622eced0-8196-4da1-a370-70dc87be5596",
                "SITES": {
                    "www.oxfam.org.uk": {
                        "CDN_PROFILE_NAME": "oxfam",
                        "CDN_ENDPOINT_NAME": "oxfam-main-site",
                    },
                    "volunteer.oxfam.org.uk": {
                        "CDN_PROFILE_NAME": "volunteering",
                        "CDN_ENDPOINT_NAME": "volunteer-oxfam",
                    },
                },
            }
        )
        self.assertEqual(
            backend._get_setting_for_hostname("www.oxfam.org.uk", "cdn_profile_name"),
            "oxfam",
        )
        self.assertEqual(
            backend._get_setting_for_hostname("www.oxfam.org.uk", "cdn_endpoint_name"),
            "oxfam-main-site",
        )
        self.assertEqual(
            backend._get_setting_for_hostname(
                "www.oxfam.org.uk", "resource_group_name"
            ),
            "oxfam-production",
        )
        self.assertEqual(
            backend._get_setting_for_hostname("www.oxfam.org.uk", "subscription_id"),
            "622eced0-8196-4da1-a370-70dc87be5596",
        )
        self.assertEqual(
            backend._get_setting_for_hostname(
                "volunteer.oxfam.org.uk", "subscription_id"
            ),
            "622eced0-8196-4da1-a370-70dc87be5596",
        )

        self.assertEqual(
            backend._get_setting_for_hostname(
                "volunteer.oxfam.org.uk", "cdn_profile_name"
            ),
            "volunteering",
        )
        self.assertEqual(
            backend._get_setting_for_hostname(
                "volunteer.oxfam.org.uk", "cdn_endpoint_name"
            ),
            "volunteer-oxfam",
        )

    def test_multi_site_inheritance(self):
        backend = AzureCdnBackend(
            {
                "RESOURCE_GROUP_NAME": "oxfam-production",
                "SUBSCRIPTION_ID": "622eced0-8196-4da1-a370-70dc87be5596",
                "SITES": {
                    "www.oxfam.org.uk": {
                        "CDN_PROFILE_NAME": "oxfam",
                        "CDN_ENDPOINT_NAME": "oxfam-main-site",
                    },
                    "volunteer.oxfam.org.uk": {
                        "RESOURCE_GROUP_NAME": "oxfam-volunteering",
                        "CDN_PROFILE_NAME": "volunteering",
                        "CDN_ENDPOINT_NAME": "volunteer-oxfam",
                    },
                },
            }
        )
        self.assertEqual(
            backend._get_setting_for_hostname(
                "www.oxfam.org.uk", "resource_group_name"
            ),
            "oxfam-production",
        )
        self.assertEqual(
            backend._get_setting_for_hostname(
                "volunteer.oxfam.org.uk", "resource_group_name"
            ),
            "oxfam-volunteering",
        )

    def test_multi_site_missing_setting_raises(self):
        backend = AzureCdnBackend(
            {
                "SUBSCRIPTION_ID": "622eced0-8196-4da1-a370-70dc87be5596",
                "SITES": {
                    "www.oxfam.org.uk": {
                        "CDN_PROFILE_NAME": "oxfam",
                        "CDN_ENDPOINT_NAME": "oxfam-main-site",
                    },
                    "volunteer.oxfam.org.uk": {
                        "RESOURCE_GROUP_NAME": "oxfam-volunteering",
                        "CDN_PROFILE_NAME": "volunteering",
                        "CDN_ENDPOINT_NAME": "volunteer-oxfam",
                    },
                },
            }
        )
        self.assertEqual(
            backend._get_setting_for_hostname(
                "volunteer.oxfam.org.uk", "resource_group_name"
            ),
            "oxfam-volunteering",
        )
        with self.assertRaisesRegex(
            ImproperlyConfigured,
            "Missing Azure CDN front-end cache invalidator for setting: "
            r"resource_group_name \(www.oxfam.org.uk\)",
        ):
            backend._get_setting_for_hostname("www.oxfam.org.uk", "resource_group_name")

    def test_filter_urls_by_hostname(self):
        backend = AzureCdnBackend({})
        fake = Faker()
        # Faker may return repeated URLs so make it a set.
        fake_urls = frozenset(fake.uri() for _ in range(2000))
        filtered_urls = backend._filter_urls_by_hostname(fake_urls)
        self.assertEqual(
            len([item for sublist in filtered_urls.values() for item in sublist]),
            len(fake_urls),
        )
