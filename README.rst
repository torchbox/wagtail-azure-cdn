THIS PACKAGE IS BEING MERGED INTO WAGTAIL ITSELF
==============================================

See the documentation at https://docs.wagtail.org/en/stable/reference/contrib/frontendcache.html.

https://github.com/wagtail/wagtail/pull/8448 needs to be merged first in order for Wagtail to be using up to date Azure SDK that this package is using. You may want to hold off using the Wagtail version until that happens.

This package won't be actively maintainted.

wagtail-azure-cdn
=================

An Azure CDN or Front Door backend for Wagtail's
`front-end cache invalidator <https://docs.wagtail.io/en/latest/reference/contrib/frontendcache.html>`_.

This module requires `azure-mgmt-cdn
<https://pypi.org/project/azure-mgmt-cdn/>`_ as minimum to work properly with Azure CDN.


This module requires `azure-mgmt-frontdoor
<https://pypi.org/project/azure-mgmt-frontdoor/>`_ as minimum to work properly with Azure Front Door.


Installation
------------

.. code:: shell

   pip install wagtail-azure-cdn

You can also install with dependencies. For Azure CDN support:

.. code:: shell

   pip install wagtail-azure-cdn[cdn]

Or for Front Door support:

.. code:: shell

   pip install wagtail-azure-cdn[frontdoor]

Or for both:

.. code:: shell

   pip install wagtail-azure-cdn[cdn,frontdoor]


Configuration for Azure CDN
---------------------------

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


Configuration for Azure Front Door
----------------------------------

Add the following settings to your Wagtail project.

.. code:: python

    from azure.common.credentials import get_azure_cli_credentials

    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail_azure_cdn.backends.AzureFrontDoorBackend",
            "RESOURCE_GROUP_NAME": "Your resource group name",
            "FRONTDOOR_NAME": "Your Front Door name",
            "SUBSCRIPTION_ID": "Your subscription ID",
            "CREDENTIALS": get_azure_cli_credentials()[0]
        }
    }


* ``RESOURCE_GROUP_NAME``, ``FRONTDOOR_NAME`` and ``SUBSCRIPTION_ID`` can be all
  obtained from the Azure portal.
* ``CREDENTIALS`` is Azure credentials objects. They may be a callable to. `See
  the documentation
  <https://docs.microsoft.com/en-us/azure/python/python-sdk-azure-authenticate>`_
  for the details.

Multi-site configuration
~~~~~~~~~~~~~~~~~~~~~~~~

The multi-site configuration works the same for the Front Door, just use ``SITES``.


.. code:: python

    from azure.common.credentials import get_azure_cli_credentials

    WAGTAILFRONTENDCACHE = {
        "default": {
            "BACKEND": "wagtail_azure_cdn.backends.AzureFrontDoorBackend",
            "SITES": {
                "torchbox.com": {
                    "RESOURCE_GROUP_NAME": "Your resource group name",
                    "FRONTDOOR_NAME": "Your Front Door name",
                    "SUBSCRIPTION_ID": "Your subscription ID",
                    "CREDENTIALS": get_azure_cli_credentials()[0],
                },
            },
        },
    }
