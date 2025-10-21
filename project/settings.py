import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "YGYdgyUFaX1mAx954wyUzqV5a1nzSR0w1bSLNLeTe_xLEpNNJvf6zItxo7unaaEfrYs")

DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",") if os.getenv("DJANGO_ALLOWED_HOSTS") else ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "weather",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "weather_db"),
        "USER": os.environ.get("DB_USER", "weather_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 600,
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

ECOWITT_SHARED_TOKEN = os.getenv("ECOWITT_SHARED_TOKEN", "changeme_token")
ECOWITT_ALLOWED_IPS = os.getenv("ECOWITT_ALLOWED_IPS", "").split(",") if os.getenv("ECOWITT_ALLOWED_IPS") else []
# --- added: ensure project-level templates dir is included in TEMPLATES ---
try:
    # ensure BASE_DIR exists; otherwise define a reasonable fallback
    BASE_DIR  # noqa: F401
except NameError:
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent

# Add BASE_DIR / "templates" to TEMPLATES[*]["DIRS"] if not present.
# This runs at import-time after the original TEMPLATES is defined.
try:
    for tpl in TEMPLATES:
        dirs = tpl.get("DIRS")
        tpl_templates_dir = BASE_DIR / "templates"
        if not dirs:
            tpl["DIRS"] = [tpl_templates_dir]
        else:
            # if path-like items may be strings or Path - normalize check by string
            if all(str(d) != str(tpl_templates_dir) for d in dirs):
                tpl["DIRS"].insert(0, tpl_templates_dir)
except Exception:
    # if anything goes wrong here, leave original settings unchanged
    pass
# --- end added ---
