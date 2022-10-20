## Authentication_API_JWT_DRF

<h3>endpoints:</h3>
<ul> 
  <li>localhost/auth/register</li> 
  <li>localhost/auth/login</li>
  <li>localhost/auth/user</li>
</ul>

<h3>permissions:</h3>
<ul> 
  <li>register : anyone</li> 
  <li>login : anyone</li>
  <li>user : need Authentication</li>
</ul>

```
more:
after user registration, system would send an email for him and he can confirm his account.
```

### installing requirements.txt:

`pip install -r requirements.txt`

### initial database:

`python manage.py makemigrations`<br/>
`python manage.py migrate`

### run Application:

`python manage.py runserver`
