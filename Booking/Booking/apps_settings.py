

DEPENDENCIES = [
    'crispy_forms',
    'allauth', # Django-allauth apps
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', # Social/third party login provider for Digital Ocean
]

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',]

GENERATED_APPS = [
    'Hotel',
    ]

INSTALLED_APPS = BASE_APPS + DEPENDENCIES + GENERATED_APPS