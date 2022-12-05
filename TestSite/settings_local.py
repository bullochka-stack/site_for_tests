from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-g@)y!^=1ds+jc&u7^4&-=!_odrlyo_qni^y+j!m_3q7afoetor'
DEBUG = True
ALLOWED_HOSTS = []
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
