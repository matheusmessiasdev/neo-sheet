from .settings import *  # noqa

# Memory Cache for tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'neo-sheet-test-cache',
    }
}
