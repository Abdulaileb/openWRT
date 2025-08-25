# Local test configuration
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Local paths for testing
LOCAL_BUFFER_FILE = os.path.join(BASE_DIR, "test_logs.txt")
LOCAL_SIGNED_DIR = os.path.join(BASE_DIR, "signed_logs")
LOCAL_KEY_DIR = os.path.join(BASE_DIR, "keys")

# Ensure directories exist
os.makedirs(LOCAL_SIGNED_DIR, exist_ok=True)
os.makedirs(LOCAL_KEY_DIR, exist_ok=True)

# Key files for testing
TEST_KEY_FILE = os.path.join(LOCAL_KEY_DIR, "test_signing.key")
TEST_PUBLIC_KEY_FILE = os.path.join(LOCAL_KEY_DIR, "test_signing.pub")