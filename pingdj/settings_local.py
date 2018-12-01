DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pingdj',
        'USER': 'mitnk',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = [
    '192.168.195.61',
]

INTERNAL_IPS = [
    '192.168.195.61',
]
