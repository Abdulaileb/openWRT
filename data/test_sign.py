# import time
# import json
# import hashlib
# from nacl.signing import SigningKey

# # Generate temporary test key
# signing_key = SigningKey.generate()

# def sign_log(log_entry: dict):
#     """Sign a single JSON log entry"""
#     log_str = json.dumps(log_entry, sort_keys=True)  # stable serialization
#     timestamp = str(time.time())
#     message_id = hashlib.sha256((timestamp + log_str).encode()).hexdigest()[:16]
#     data_to_sign = f"{message_id}{timestamp}{log_str}".encode()
#     signature = signing_key.sign(data_to_sign).signature
#     return {
#         "message_id": message_id,
#         "timestamp": timestamp,
#         "log_entry": log_entry,
#         "signature": signature.hex()
#     }

# def benchmark_signing(log_file: str):
#     """Load JSON logs, sign each entry, and report speed"""
#     with open(log_file, "r") as f:
#         doc = json.load(f)

#     logs = []
#     if "logs" in doc:  # batch style
#         logs = doc["logs"]
#     else:  # flat structure
#         logs = doc

#     start = time.perf_counter()
#     signed_logs = [sign_log(log) for log in logs]
#     end = time.perf_counter()

#     elapsed = end - start
#     rate = len(logs) / elapsed if elapsed > 0 else float("inf")

#     print(f"✅ Signed {len(logs)} logs in {elapsed:.4f}s")
#     print(f"⚡ Throughput: {rate:.2f} logs/sec")

#     return signed_logs

# if __name__ == "__main__":
#     signed = benchmark_signing("synthetic_100k_logs.json")


import time
import json
import hashlib
import os
from pathlib import Path
from nacl.signing import SigningKey

# Generate temporary test key
signing_key = SigningKey.generate()

OUTPUT_DIR = "signed_batches"
BATCH_SIZE = 20000

def sign_log(log_entry: dict):
    """Sign a single JSON log entry"""
    log_str = json.dumps(log_entry, sort_keys=True)  # stable serialization
    timestamp = str(time.time())
    message_id = hashlib.sha256((timestamp + log_str).encode()).hexdigest()[:16]
    data_to_sign = f"{message_id}{timestamp}{log_str}".encode()
    signature = signing_key.sign(data_to_sign).signature
    return {
        "message_id": message_id,
        "timestamp": timestamp,
        "log_entry": log_entry,
        "signature": signature.hex()
    }

def benchmark_and_batch(log_file: str):
    """Load JSON logs, sign each entry, save them into 100-log batches"""
    with open(log_file, "r") as f:
        doc = json.load(f)

    logs = doc.get("logs", doc)  # handle both {"logs": [...]} and [...] formats

    start = time.perf_counter()
    signed_logs = [sign_log(log) for log in logs]
    end = time.perf_counter()

    elapsed = end - start
    rate = len(logs) / elapsed if elapsed > 0 else float("inf")

    print(f"✅ Signed {len(logs)} logs in {elapsed:.4f}s")
    print(f"⚡ Throughput: {rate:.2f} logs/sec")

    # --- Save in batches ---
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    for i in range(0, len(signed_logs), BATCH_SIZE):
        batch = signed_logs[i:i + BATCH_SIZE]
        batch_index = (i // BATCH_SIZE) + 1
        out_file = os.path.join(OUTPUT_DIR, f"signed_batch_{batch_index}.json")

        with open(out_file, "w") as f:
            json.dump({"messages": batch}, f, indent=2)

        print(f"💾 Saved batch {batch_index} → {out_file} ({len(batch)} logs)")

    return signed_logs

if __name__ == "__main__":
    signed = benchmark_and_batch("synthetic_100k_logs.json")
