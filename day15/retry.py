import time


def retry(operation, max_attempts=3, delay_seconds=2):
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Attempt {attempt}/{max_attempts}")
            return operation()
        except Exception as error:
            last_error = error
            print(f"Attempt {attempt} failed: {error}")

            if attempt < max_attempts:
                print(f"Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)

    raise last_error