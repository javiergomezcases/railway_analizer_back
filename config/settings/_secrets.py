from config.settings.base import env

SECRET_KEY = env('SECRET_KEY', default='secret_key').strip()
POSTGRES_DB = env('POSTGRES_DB', default='').strip()
POSTGRES_USER = env('POSTGRES_USER', default='').strip()
POSTGRES_PASSWORD = env('POSTGRES_PASSWORD', default='').strip()
