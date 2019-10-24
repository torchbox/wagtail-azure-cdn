wagtail-azure-cdn
=================

An Azure CDN backend for Wagtail's
`front-end cache invalidator <https://docs.wagtail.io/en/latest/reference/contrib/frontendcache.html>`_.

This module requires `azure-mgmt-cdn
<https://pypi.org/project/azure-mgmt-cdn/>`_ as minimum to work properly.


Installation
------------

.. code:: shell

   pip install wagtail-azure-cdn


Configuration
-------------

Add the following settings to your Wagtail project.

.. code:: python

    from azure.common.credentials import get_azure_cli_credentials

    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail_azure_cdn.backends.AzureCdnBackend",
            "RESOURCE_GROUP_NAME": "Your resource group name",
            "CDN_PROFILE_NAME": "Your CDN profile name",
            "SUBSCRIPTION_ID": "Your subscription ID",
            "CDN_ENDPOINT_NAME": "Your endpoint name",
            "CREDENTIALS": get_azure_cli_credentials()[0]
        }
    }


* ``RESOURCE_GROUP_NAME``, ``CDN_PROFILE_NAME``, ``SUBSCRIPTION_ID`` and
  ``CDN_ENDPOINT_NAME`` can be all obtained from the Azure portal.
* ``CREDENTIALS`` is Azure credentials objects. They may be a callable to. `See
  the documentation
  <https://docs.microsoft.com/en-us/azure/python/python-sdk-azure-authenticate>`_
  for the details.

Multiple sites
~~~~~~~~~~~~~~

You can set settings for multiple hosts using the ``SITES`` setting , for
example:

.. code:: python

    from azure.common.credentials import get_azure_cli_credentials

    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail_azure_cdn.backends.AzureCdnBackend",
            "SITES": {
                "torchbox.com": {
                    "RESOURCE_GROUP_NAME": "Your resource group name",
                    "CDN_PROFILE_NAME": "Your CDN profile name",
                    "SUBSCRIPTION_ID": "Your subscription ID",
                    "CDN_ENDPOINT_NAME": "Your endpoint name",
                    "CREDENTIALS": get_azure_cli_credentials()[0],
                },
            },
        },
    }


Settings set at the top level will be used if there's no settings for a site.
E.g. you can do this:


.. code:: python

    from azure.common.credentials import get_azure_cli_credentials

    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail_azure_cdn.backends.AzureCdnBackend",
            "RESOURCE_GROUP_NAME": "Your resource group name",
            "CDN_PROFILE_NAME": "Your CDN profile name",
            "SUBSCRIPTION_ID": "Your subscription ID",
            "SITES": {
                "torchbox.com": {
                    "CDN_ENDPOINT_NAME": "Your endpoint name",
                    "CREDENTIALS": get_azure_cli_credentials()[0]
                },

                "jobs.torchbox.com": {
                    "CDN_ENDPOINT_NAME": "Your endpoint name",
                    "CREDENTIALS": get_azure_cli_credentials()[0]
                },
            },
        },
    }
