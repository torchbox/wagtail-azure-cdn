import logging
from urllib.parse import urlparse

from django.utils.http import is_same_domain

logger = logging.getLogger(__name__)


def use_x_host_header(get_response):
    """
    Replace HTTP_X_FORWARDED_HOST with HTTP_X_HOST if present. This is a header used by
    Azure CDN from Verizon.
    """
    def middleware(request):
        x_host = request.META.get("HTTP_X_HOST")
        if x_host:
            logger.debug("Replacing HTTP_X_FORWARDED_HOST with HTTP_X_HOST: %s", x_host)
            request.META["HTTP_X_FORWARDED_HOST"] = x_host
        return get_response(request)

    return middleware
