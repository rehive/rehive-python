# Rehive Python SDK
A tool primarly used for quick interfacing with the Rehive API.


## Install
```
pip install rehive
```

## Examples And How-to

```
from rehive import Rehive, APIException
rehive = Rehive()  # OR Rehive(API_TOKEN_HERE)
```
You can parse an api token or leave blank if manually logging in. Each object instance will store it's own token and act as another user.

Login:
```
rehive.auth.login({"user": "user", "company": "company", "password": "pass"})
```

Get:
```
rehive.admin.accounts.get()
```

Get nested objects:
```
rehive.admin.accounts.obj('5AT24mW61H').currencies.get()
```

Get with filters:
```
rehive.admin.transactions.get(filters={"status":"confirmed"})
```

Create:
```
rehive.admin.users.emails.create('1d3e584d-ac56-483c-8aa5-d4ef059608ba', 'connor+899@rehive.com', verified=True)
```

Patch/Put:
```
rehive.admin.company.switches.patch('1', enabled=True) # Patch switch with identifier 1
```

Pagination:
```
rehive.admin.currencies.get()
rehive.admin.currencies.get_next()
rehive.admin.currencies.get_previous()
```


## Exception And Error Handling

```
from rehive import APIException

try:
  rehive.admin.currencies.get()
exception APIException as e:
  print(e.status_code) # Error code status code from Rehive
  print(e.data) # Any custom error messages and data returned from Rehive
```
