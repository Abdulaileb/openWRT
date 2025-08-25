import json
import os
import random
import time
import uuid
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

LOG_DIR = "generated_logs"
os.makedirs(LOG_DIR, exist_ok=True)

class LogGenerator:
    def __init__(self):
        self.severity_levels = ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
        self.services = ["web-server", "database", "auth-service", "payment-gateway", "notification-service"]
        self.ip_ranges = ["192.168.1.", "10.0.0.", "172.16.0.", "203.0.113."]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        self.status_codes = [200, 201, 301, 400, 401, 403, 404, 500, 502, 503]
        
    def generate_siem_log(self, log_id):
        """Generate SIEM security event logs"""
        event_types = ["login_attempt", "file_access", "network_scan", "privilege_escalation", "data_exfiltration"]
        
        return {
            "event_id": f"siem_{log_id}",
            "timestamp": self.random_timestamp().isoformat(),
            "severity": random.choice(self.severity_levels),
            "event_type": random.choice(event_types),
            "source_ip": self.random_ip(),
            "destination_ip": self.random_ip(),
            "user": fake.user_name(),
            "description": f"Security event detected: {random.choice(event_types)}",
            "risk_score": random.randint(1, 100),
            "action_taken": random.choice(["blocked", "allowed", "quarantined", "logged"])
        }
    
    def generate_web_access_log(self, log_id):
        """Generate web server access logs"""
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        endpoints = ["/api/users", "/api/orders", "/login", "/dashboard", "/api/payments"]
        
        return {
            "log_id": f"web_{log_id}",
            "timestamp": self.random_timestamp().isoformat(),
            "client_ip": self.random_ip(),
            "method": random.choice(methods),
            "endpoint": random.choice(endpoints),
            "status_code": random.choice(self.status_codes),
            "response_size": random.randint(200, 50000),
            "response_time_ms": random.randint(10, 5000),
            "user_agent": random.choice(self.user_agents),
            "referer": fake.url() if random.random() > 0.3 else None
        }
    
    def generate_application_log(self, log_id):
        """Generate application logs"""
        components = ["UserService", "OrderProcessor", "PaymentHandler", "EmailSender", "DatabaseConnector"]
        actions = ["processing_request", "database_query", "external_api_call", "cache_update", "validation_check"]
        
        return {
            "log_id": f"app_{log_id}",
            "timestamp": self.random_timestamp().isoformat(),
            "level": random.choice(self.severity_levels),
            "service": random.choice(self.services),
            "component": random.choice(components),
            "action": random.choice(actions),
            "message": f"Processing {random.choice(actions)} for {fake.word()}",
            "execution_time_ms": random.randint(1, 1000),
            "memory_usage_mb": random.randint(50, 512),
            "thread_id": random.randint(1, 20)
        }
    
    def generate_database_log(self, log_id):
        """Generate database operation logs"""
        operations = ["SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP"]
        tables = ["users", "orders", "products", "payments", "audit_log"]
        
        return {
            "log_id": f"db_{log_id}",
            "timestamp": self.random_timestamp().isoformat(),
            "database": random.choice(["production", "staging", "analytics"]),
            "operation": random.choice(operations),
            "table": random.choice(tables),
            "rows_affected": random.randint(0, 1000),
            "query_time_ms": random.randint(1, 5000),
            "connection_id": random.randint(1, 100),
            "user": f"db_user_{random.randint(1, 10)}",
            "query_hash": fake.sha256()[:16]
        }
    
    def generate_system_log(self, log_id):
        """Generate system/infrastructure logs"""
        metrics = ["cpu_usage", "memory_usage", "disk_io", "network_throughput", "process_count"]
        hosts = ["web-01", "db-01", "cache-01", "lb-01", "worker-01"]
        
        return {
            "log_id": f"sys_{log_id}",
            "timestamp": self.random_timestamp().isoformat(),
            "hostname": random.choice(hosts),
            "metric": random.choice(metrics),
            "value": round(random.uniform(0, 100), 2),
            "unit": random.choice(["%", "MB", "GB", "req/s", "ms"]),
            "alert_threshold": random.randint(80, 95),
            "status": random.choice(["normal", "warning", "critical"]),
            "pid": random.randint(1000, 9999)
        }
    
    def generate_error_log(self, log_id):
        """Generate error/exception logs"""
        error_types = ["NullPointerException", "SQLException", "TimeoutException", "AuthenticationError", "ValidationError"]
        
        return {
            "error_id": f"err_{log_id}",
            "timestamp": self.random_timestamp().isoformat(),
            "severity": random.choice(["ERROR", "CRITICAL"]),
            "error_type": random.choice(error_types),
            "message": f"Error occurred in {random.choice(self.services)}: {fake.sentence()}",
            "stack_trace": self.generate_stack_trace(),
            "user_id": fake.uuid4() if random.random() > 0.5 else None,
            "session_id": fake.uuid4(),
            "request_id": fake.uuid4()
        }
    
    def random_timestamp(self):
        """Generate random timestamp within last 30 days"""
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        random_seconds = random.randrange(86400)  # seconds in a day
        return start_date + timedelta(days=random_days, seconds=random_seconds)
    
    def random_ip(self):
        """Generate random IP address"""
        return random.choice(self.ip_ranges) + str(random.randint(1, 254))
    
    def generate_stack_trace(self):
        """Generate fake stack trace"""
        lines = []
        for i in range(random.randint(3, 8)):
            lines.append(f"    at {fake.word()}.{fake.word()}({fake.word()}.java:{random.randint(10, 500)})")
        return "\\n".join(lines)

def generate_mixed_logs(total_count=1000, batch_size=100):
    """Generate mixed types of logs and save to batch files"""
    generator = LogGenerator()
    
    log_types = [
        generator.generate_siem_log,
        generator.generate_web_access_log,
        generator.generate_application_log,
        generator.generate_database_log,
        generator.generate_system_log,
        generator.generate_error_log
    ]
    
    logs = []
    batch_num = 1
    
    for i in range(1, total_count + 1):
        # Randomly select log type
        log_func = random.choice(log_types)
        log_entry = log_func(i)
        logs.append(log_entry)
        
        # Save batch when reaching batch_size
        if i % batch_size == 0:
            batch_file = os.path.join(LOG_DIR, f"mixed_batch_{batch_num}.json")
            with open(batch_file, "w") as f:
                json.dump({
                    "batch_info": {
                        "batch_number": batch_num,
                        "total_logs": len(logs),
                        "generated_at": datetime.now().isoformat(),
                        "log_types": list(set([log.get("log_id", log.get("event_id", log.get("error_id", "unknown"))).split("_")[0] for log in logs]))
                    },
                    "logs": logs
                }, f, indent=2)
            
            print(f"✅ Saved batch {batch_num} with {len(logs)} logs to {batch_file}")
            logs = []
            batch_num += 1
    
    # Save remaining logs if any
    if logs:
        batch_file = os.path.join(LOG_DIR, f"mixed_batch_{batch_num}.json")
        with open(batch_file, "w") as f:
            json.dump({
                "batch_info": {
                    "batch_number": batch_num,
                    "total_logs": len(logs),
                    "generated_at": datetime.now().isoformat()
                },
                "logs": logs
            }, f, indent=2)
        print(f"✅ Saved final batch {batch_num} with {len(logs)} logs to {batch_file}")

def generate_specific_log_type(log_type, count=100):
    """Generate logs of a specific type"""
    generator = LogGenerator()
    
    type_map = {
        "siem": generator.generate_siem_log,
        "web": generator.generate_web_access_log,
        "app": generator.generate_application_log,
        "db": generator.generate_database_log,
        "system": generator.generate_system_log,
        "error": generator.generate_error_log
    }
    
    if log_type not in type_map:
        print(f"❌ Unknown log type: {log_type}")
        print(f"Available types: {list(type_map.keys())}")
        return
    
    logs = []
    log_func = type_map[log_type]
    
    for i in range(1, count + 1):
        logs.append(log_func(i))
    
    filename = os.path.join(LOG_DIR, f"{log_type}_logs_{count}.json")
    with open(filename, "w") as f:
        json.dump({
            "log_type": log_type,
            "total_count": count,
            "generated_at": datetime.now().isoformat(),
            "logs": logs
        }, f, indent=2)
    
    print(f"✅ Generated {count} {log_type} logs in {filename}")

if __name__ == "__main__":
    print("🔹 Log Generator Starting...")
    
    # Generate mixed logs (default)
    print("\n📊 Generating mixed log types...")
    generate_mixed_logs(1000, batch_size=100)  # 10 files, 100 logs each
    
    # Generate specific log types
    print("\n🎯 Generating specific log types...")
    for log_type in ["siem", "web", "app", "db", "system", "error"]:
        generate_specific_log_type(log_type, 200)
    
    print(f"\n✅ All logs generated successfully!")
    print(f"📁 Check the '{LOG_DIR}' directory for your log files.")
    
    # Display summary
    files = os.listdir(LOG_DIR)
    print(f"\n📋 Generated {len(files)} files:")
    for file in sorted(files):
        file_path = os.path.join(LOG_DIR, file)
        size_kb = round(os.path.getsize(file_path) / 1024, 2)
        print(f"   • {file} ({size_kb} KB)")