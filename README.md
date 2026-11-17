# Random Number Generator Microservice

This is a simple Python microservice I made for my CS361 project. It uses Flask to generate random numbers, make unique IDs, and shuffle numbers. Other programs can send requests to it and get the results back as JSON.

## Files and Setup

- `app.py` - the microservice code.
- Python packages needed: `flask` (and `requests` if you want to use the example client code below).

To set it up in PyCharm, open the project and install Flask in the terminal:

```bash
python -m pip install flask
```

Run `app.py` to start the microservice. It runs at `http://127.0.0.1:5002`. Leave it running while another program uses it. Press Ctrl+C to stop it.

## Communication Contract

The microservice uses HTTP requests and JSON responses. The other program sends a request to one of these endpoints:

| Endpoint | Method | What it does |
| --- | --- | --- |
| `/random` | GET | Returns a random whole number between `min` and `max`. Both are included. Defaults to 0 and 100. |
| `/generate-id` | GET | Returns a new unique ID as a string. |
| `/shuffle` | POST | Takes a number `n`, creates a list from 0 to `n - 1`, and shuffles it. |

### How to request data

These examples use the `requests` library, which you can install with `python -m pip install requests` in the program making the requests.

**Get a random number between 1 and 20:**

```python
import requests

response = requests.get('http://127.0.0.1:5002/random', params={'min': 1, 'max': 20})
print(response.json())
```

**Get a unique ID:**

```python
response = requests.get('http://127.0.0.1:5002/generate-id')
print(response.json())
```

**Get five numbers in a random order:**

```python
response = requests.post('http://127.0.0.1:5002/shuffle', json={'n': 5})
print(response.json())
```

The shuffle request needs a JSON object with `n` set to a whole number from 0 to 100000. It does not shuffle a list that you send in.

### How to receive data

Successful responses contain `status` and `result`. Here are some example responses:

**Random number:**

```json
{"status": "success", "result": 12}
```

**Unique ID:**

```json
{"status": "success", "result": "f47ac10b58cc4372a5670e02b2c3d479"}
```

**Shuffled numbers:**

```json
{"status": "success", "result": [3, 0, 4, 1, 2]}
```

The values will usually be different each time. To get the result in Python, use:

```python
result = response.json()['result']
```

If the request is invalid, the microservice returns HTTP error code 400 with `status` set to `error` and an `error` message. For example, if `min` is greater than `max`:

```json
{"status": "error", "error": "min cannot be greater than max"}
```

The `/random` endpoint needs `min` and `max` to be numbers that can be converted to integers. The `/shuffle` endpoint needs `n` to be an integer from 0 to 100000.

## How It Works

1. Start `app.py`.
2. Another program sends an HTTP request to the microservice.
3. The microservice runs the requested function using Python's `random` or `uuid` module.
4. It sends the result back as JSON.
5. The other program reads the result and uses it.

The microservice and the program using it run separately. Both need to be running for requests to work.
