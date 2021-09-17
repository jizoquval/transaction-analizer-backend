# transaction-analizer-backend

## Run app

```
pipenv install
pipenv shell
gunicorn wsgi:app --timeout 180
```