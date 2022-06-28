from config.settings.base import env

DEBUG = env('DEBUG', default=False)
POSTGRES_HOST = env('POSTGRES_HOST', default='').strip()
POSTGRES_PORT = env('POSTGRES_PORT', default='')
