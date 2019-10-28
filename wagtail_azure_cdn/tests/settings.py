import os

DEBUG = False
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, "tests", "test-static")
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "tests", "test-media")
MEDIA_URL = "/media/"

TIME_ZONE = "Asia/Tokyo"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "db.sqlite3"}}

SECRET_KEY = "not needed"

ROOT_URLCONF = "wagtail_azure_cdn.tests.urls"

STATIC_URL = "/static/"

STATICFILES_FINDERS = ("django.contrib.staticfiles.finders.AppDirectoriesFinder",)

USE_TZ = True

LANGUAGE_CODE = "en"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "wagtail.tests.context_processors.do_not_use_static_url",
                "wagtail.contrib.settings.context_processors.settings",
            ]
        },
    }
]

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
)

INSTALLED_APPS = (
    "wagtail.contrib.styleguide",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.frontend_cache",
    "wagtail.contrib.redirects",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.settings",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.table_block",
    "wagtail.contrib.forms",
    "wagtail.search",
    "wagtail.embeds",
    "wagtail.images",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.admin",
    "wagtail.api.v2",
    "wagtail.core",
    "taggit",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
)


# Using DatabaseCache to make sure that the cache is cleared between tests.
# This prevents false-positives in some wagtail core tests where we are
# changing the 'wagtail_root_paths' key which may cause future tests to fail.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
    }
}

PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

ALLOWED_HOSTS = ["localhost", "testserver"]

WAGTAILSEARCH_BACKENDS = {"default": {"BACKEND": "wagtail.search.backends.db"}}

WAGTAIL_SITE_NAME = "Test Site"

SILENCED_SYSTEM_CHECKS = ["wagtailadmin.W001"]
