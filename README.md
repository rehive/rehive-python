# Rehive Python SDK

A Python SDK for the Rehive Platform API.

## Install

```shell
pip install rehive
```

## Documentation

For documentation on the Rehive ecosystem: [Docs Portal](https://docs.rehive.com/)

For the full Rehive Platform API specification: [API Reference](https://docs.platform.rehive.com/)

## Usage

```python
from rehive import Rehive, APIException
rehive = Rehive()  # OR Rehive(API_TOKEN_HERE)
```
You can parse an api token or leave blank if manually logging in. Each object instance will store it's own token and act as another user.

Auth:

```python
rehive = Rehive(REHIVE_API_KEY)
```

Get:

```python
rehive.admin.accounts.get()
```

Get nested objects:

```python
rehive.admin.accounts.obj('5AT24mW61H').currencies.get()
```

Get with filters:

```python
rehive.admin.transactions.get(filters={"status":"complete"})
```

Create:

```python
rehive.admin.users.emails.create('1d3e584d-ac56-483c-8aa5-d4ef059608ba', 'connor+899@rehive.com', verified=True)
```

Patch/Put:

```python
rehive.admin.company.switches.patch('1', enabled=True) # Patch switch with identifier 1
```

Pagination:

```python
rehive.admin.currencies.get()
rehive.admin.currencies.get_next()
rehive.admin.currencies.get_previous()
```


## Exception And Error Handling

```python
from rehive import APIException

try:
  rehive.admin.currencies.get()
except APIException as e:
  print(e.status_code) # Error code status code from Rehive
  print(e.data) # Any custom error messages and data returned from Rehive
```

## Idempotent requests

```python
rehive.user.update(last_name='test7777', idempotent_key='{UNIQUE_KEY}')
```
