import requests

BASE_URL = "http://127.0.0.1:5002"

passed = 0
failed = 0


def record_result(name, success):
    global passed, failed

    if success:
        print("TEST PASSED:", name)
        passed += 1
    else:
        print("TEST FAILED:", name)
        failed += 1

    print()


# TEST 1: generate a random number
print("TEST 1: Random Number Generation")

try:
    response = requests.get(
        f"{BASE_URL}/random",
        params={"min": 1, "max": 20}
    )
    data = response.json()
    number = data.get("result")

    print("Response:", data)

    success = (
        response.status_code == 200
        and data.get("status") == "success"
        and isinstance(number, int)
        and 1 <= number <= 20
    )

    record_result("Random number between 1 and 20", success)

except requests.RequestException as error:
    print("Connection error:", error)
    record_result("Random number between 1 and 20", False)


# TEST 2: generate a unique ID
print("TEST 2: Unique ID Generation")

try:
    response = requests.get(f"{BASE_URL}/generate-id")
    data = response.json()
    identifier = data.get("result")

    print("Response:", data)

    success = (
        response.status_code == 200
        and data.get("status") == "success"
        and isinstance(identifier, str)
        and len(identifier) > 0
        and identifier.isalnum()
    )

    record_result("Valid alphanumeric ID", success)

except requests.RequestException as error:
    print("Connection error:", error)
    record_result("Valid alphanumeric ID", False)


# TEST 3: shuffle a list
print("TEST 3: Shuffle Index List")

try:
    n = 5

    response = requests.post(
        f"{BASE_URL}/shuffle",
        json={"n": n}
    )
    data = response.json()
    result = data.get("result")

    print("Response:", data)

    success = (
        response.status_code == 200
        and data.get("status") == "success"
        and isinstance(result, list)
        and len(result) == n
        and sorted(result) == list(range(n))
    )

    record_result("Valid shuffled list", success)

except requests.RequestException as error:
    print("Connection error:", error)
    record_result("Valid shuffled list", False)


# TEST 4: reject an inverted random range
print("TEST 4: Invalid Random Range")

try:
    response = requests.get(
        f"{BASE_URL}/random",
        params={"min": 20, "max": 5}
    )
    data = response.json()

    print("Response:", data)

    success = (
        response.status_code == 400
        and data.get("status") == "error"
    )

    record_result("Reject inverted random range", success)

except requests.RequestException as error:
    print("Connection error:", error)
    record_result("Reject inverted random range", False)


# TEST 5: reject non-integer shuffle input
print("TEST 5: Invalid Shuffle Input")

try:
    response = requests.post(
        f"{BASE_URL}/shuffle",
        json={"n": "five"}
    )
    data = response.json()

    print("Response:", data)

    success = (
        response.status_code == 400
        and data.get("status") == "error"
    )

    record_result("Reject non-integer shuffle input", success)

except requests.RequestException as error:
    print("Connection error:", error)
    record_result("Reject non-integer shuffle input", False)


# TEST 6: reject missing shuffle input
print("TEST 6: Missing Shuffle Input")

try:
    response = requests.post(
        f"{BASE_URL}/shuffle",
        json={}
    )
    data = response.json()

    print("Response:", data)

    success = (
        response.status_code == 400
        and data.get("status") == "error"
    )

    record_result("Reject missing shuffle input", success)

except requests.RequestException as error:
    print("Connection error:", error)
    record_result("Reject missing shuffle input", False)


# FINAL SUMMARY
print("=" * 45)
print("RNG MICROSERVICE TEST SUMMARY")
print("=" * 45)
print("Tests passed:", passed)
print("Tests failed:", failed)
print("Total tests:", passed + failed)

if failed == 0:
    print("\nALL TESTS PASSED!")
else:
    print("\nSOME TESTS FAILED.")