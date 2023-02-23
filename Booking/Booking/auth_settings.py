AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '1032985327133-moafsbv028nuatij1jbit9c7jjgeqg86.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

# Sets the ID of your site's URL. 
SITE_ID = 1

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home' 

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
	  'allauth.account.auth_backends.AuthenticationBackend',
    ]

# ACCOUNT_SIGNUP_FORM_CLASS = 'Hotel.forms.CustomSignupForm'
