# Email Auth Config
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = True


# Email Config
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'cse.14bcs1129@gmail.com'
EMAIL_HOST_PASSWORD = 'ktivdrsbwxfofkkd'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

ACCOUNT_USERNAME_BLACKLIST = ['administrator', 'help',
                              'helpdesk', 'operator',
                              'root', 'superadmin',
                              'superuser', 'info@',
                              'admin', 'webmaster',
                              'areariservata', 'blog'
                              '@', 'master']
                              # Ban a list of names as a choice
