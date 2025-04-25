import sentry_sdk
import random
import traceback
import os
from typing import Dict, List, Optional

# Environment variable to control error triggering
TRIGGER_TEST_ERROR = os.environ.get("TRIGGER_TEST_ERROR", "true").lower() == "true"

class CustomError(Exception):
    """Custom error class for demonstration purposes."""
    pass

def process_data(data: Optional[Dict]) -> List[str]:
    """Process data and return results."""
    if data is None:
        raise ValueError("Data cannot be None")
    
    if "items" not in data:
        raise KeyError("Missing 'items' key in data")
    
    items = data["items"]
    results = []
    
    for idx, item in enumerate(items):
        if not isinstance(item, str):
            raise TypeError(f"Item at index {idx} is not a string")
        
        # Sometimes trigger a custom error
        if item.startswith("error_"):
            raise CustomError(f"Found error marker in item: {item}")
            
        results.append(item.upper())
    
    return results

def complex_error_scenario():
    """Generate a complex error scenario based on random conditions."""
    error_type = random.randint(1, 5)
    
    try:
        if error_type == 1:
            # Case 1: None data
            process_data(None)
        elif error_type == 2:
            # Case 2: Missing key
            process_data({"wrong_key": []})
        elif error_type == 3:
            # Case 3: Wrong type in list
            process_data({"items": ["valid", 123, "also_valid"]})
        elif error_type == 4:
            # Case 4: Custom error
            process_data({"items": ["valid", "error_trigger", "also_valid"]})
        else:
            # Case 5: Index error via access
            my_list = [1, 2, 3]
            print(my_list[10])
    except Exception as e:
        # Capture exception with extra context
        sentry_sdk.set_context("error_context", {
            "error_type": error_type,
            "error_name": type(e).__name__,
            "traceback": traceback.format_exc()
        })
        # Re-raise to trigger Sentry capture
        raise

def main():
    print("Hello from sentry-test!")
    
    if TRIGGER_TEST_ERROR:
        try:
            division_by_zero = 1 / 0
        except ZeroDivisionError as e:
            sentry_sdk.set_context("error_info", {
                "type": "test_error",
                "purpose": "Sentry integration testing"
            })
            raise
    else:
        print("Test error disabled. Set TRIGGER_TEST_ERROR=true to generate a test error.")


sentry_sdk.init(
    dsn="https://7d4d087faa404bd5e11792526ab12705@o4509191222460416.ingest.us.sentry.io/4509191229538304",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Add more context to help with debugging
    traces_sample_rate=1.0,
    enable_tracing=True,
)

if __name__ == "__main__":
    main()