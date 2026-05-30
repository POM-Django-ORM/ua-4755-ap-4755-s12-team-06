# Django_ORM

## install requirement project's packages

```commandline
pip install -r requirements.txt
```
Go to the folder `.github/workflows/`

Delete file `classroom.yml` and rename file `___classroom.yml` to `classroom.yml`

#### DB settings

for use local DB create file `library/library/local_settings.py` file and put this code there with your connection data
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Run project

Go to the folder with manage.py file, run library


```commandline
python manage.py runserver
```
 

## Run tests

Go to the folder with manage.py file, run library

```commandline
python manage.py test
```

## Tasks
Add the required fields to the models.
Implement methods according to docstring  for them.
