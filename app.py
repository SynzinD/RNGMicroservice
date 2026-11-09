"""
Random Number Generator Microservice

This Flask service provides random numbers, unique IDs, and shuffled lists.
Clients can choose the number range, such as 1-4 or 1-20.
The service runs locally on port 5002 and returns JSON responses.
"""

import random
import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)
MAX_SHUFFLE_SIZE = 100000


@app.get('/random')
def random_number():
    """Return a random integer between the client's minimum and maximum."""
    try:
        minimum = int(request.args.get('min', 0))
        maximum = int(request.args.get('max', 100))
    except ValueError:
        return jsonify(status='error', error='min and max must be integers'), 400

    if minimum > maximum:
        return jsonify(status='error', error='min cannot be greater than max'), 400

    number = random.randint(minimum, maximum)
    return jsonify(status='success', result=number)


@app.get('/generate-id')
def generate_id():
    """Return a new UUID identifier as a string."""
    identifier = uuid.uuid4().hex
    return jsonify(status='success', result=identifier)


@app.post('/shuffle')
def shuffle():
    """Return a shuffled list containing every index from 0 to n - 1."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or 'n' not in data:
        return jsonify(status='error', error='A JSON object with n is required'), 400

    # Only accept whole numbers, not decimals, strings, or booleans.
    n = data['n']
    if type(n) is not int:
        return jsonify(status='error', error='n must be an integer'), 400

    if n < 0 or n > MAX_SHUFFLE_SIZE:
        return jsonify(status='error', error='n must be between 0 and 100000'), 400

    indices = list(range(n))
    random.shuffle(indices)
    return jsonify(status='success', result=indices)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=False)
