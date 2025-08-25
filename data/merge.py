# import json, glob

# merged = []
# for file in glob.glob("generated_logs/new/*.json"):
#     with open(file) as f:
#         doc = json.load(f)
#         merged.extend(doc.get("logs", []))

# with open("merged_logs.json", "w") as f:
#     json.dump(merged, f, indent=2)

# print(f"✅ Merged {len(merged)} logs")




import json

def generate_logs(n, start_index=0, log_type="test"):
    logs = []
    for i in range(start_index, start_index + n):
        logs.append({
            "log_id": f"{log_type}_{i}",
            "timestamp": "2025-08-26T12:00:00.000000",
            "level": "INFO",
            "event": f"{log_type}_event_{i}",
            "src_ip": f"192.168.{i%255}.{i%255}",
            "dst_ip": f"10.0.{i%255}.{i%255}",
            "message": f"Synthetic log {i}"
        })
    return logs

# Generate 100k logs
all_logs = generate_logs(100_000)

# Save as JSON file
with open("synthetic_100k_logs.json", "w") as f:
    json.dump({"logs": all_logs}, f, indent=2)

print("✅ Generated 10,000 synthetic logs")
