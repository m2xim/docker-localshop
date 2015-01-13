DATABASES = {
    'default': {
        'ENGINE': '${database_engine}',
        'NAME': '${database_name}',
        'USER': '${database_user}',
        'PASSWORD': '${database_password}',
        'HOST': '${database_host}',
        'PORT': '${database_port}',
    }
}

TIME_ZONE = '${timezone}'

PROJECT_ROOT = '/home/localshop/data'

LOCALSHOP_DELETE_FILES=${delete_files}