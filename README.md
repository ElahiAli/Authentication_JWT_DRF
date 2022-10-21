## Authentication_API_JWT_DRF

<h3>endpoints:</h3>
<ul> 
  <li>localhost/auth/register</li> 
  <li>localhost/auth/login</li>
  <li>localhost/auth/user</li>
  <li>localhost/auth/resend-email</li>
</ul>

<h3>permissions:</h3>
<ul> 
  <li>register : anyone</li> 
  <li>login : anyone</li>
  <li>user : need Authentication</li>
  <li>resend-email : anyone</li>
</ul>

_more:_

1. after user registration, system would send an email for him and he can confirm his account.
2. without verifying account, user can not login.

### Installing requirements.txt:

```
pip install -r requirements.txt
```

### Initial Database:

```
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```
python manage.py createsuperuser
```

### Run Application:

```
python manage.py runserver
```
