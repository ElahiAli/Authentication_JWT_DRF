## Authentication_API_JWT_DRF

### Endpoints:

<ul> 
  <li>localhost/auth/register</li> 
  <li>localhost/auth/login</li>
  <li>localhost/auth/user</li>
  <li>localhost/auth/resend-email</li>
</ul>

### Permissions:

<ul> 
  <li>register : anyone</li> 
  <li>login : anyone</li>
  <li>user : need Authentication</li>
  <li>resend-email : anyone</li>
</ul>

_More:_

1. after user registration, system would send an email for him and he can confirm his account.
2. without verifying account, user can't login.
3. password can't be less than 8 and shouldn't be all numeric

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
