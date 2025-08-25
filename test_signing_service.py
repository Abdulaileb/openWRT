#!/usr/bin/env python3
import os
import time
import json
import hashlib
from datetime import datetime
from pathlib import Path
from config.test_config import *

# ✅ Use PyNaCl instead of old ed25519
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError


class LocalTestSigningService:
    def __init__(self):
        self.buffer_file = LOCAL_BUFFER_FILE
        self.signed_dir = LOCAL_SIGNED_DIR
        self.key_file = TEST_KEY_FILE
        self.public_key_file = TEST_PUBLIC_KEY_FILE
        self.key_id = "test_signer_v1"
        
        # Create test log file if it doesn't exist
        # if not os.path.exists(self.buffer_file):
        #     self.create_test_logs()
        
        # Load or generate keys
        self.load_or_generate_keys()
        
        print("🔧 Local Test Signing Service Initialized")
        print(f"   Buffer file: {self.buffer_file}")
        print(f"   Output directory: {self.signed_dir}")
        print(f"   Key ID: {self.key_id}")
    
    # def create_test_logs(self):
    #     """Create sample test logs"""
    #     test_logs = [
    #         "<134>Aug 23 14:32:00 firewall auth: SSH failed login from 192.168.1.100",
    #         "<131>Aug 23 14:32:01 firewall auth: SSH failed login from 192.168.1.100",
    #         "<130>Aug 23 14:32:02 firewall auth: SSH failed login from 192.168.1.100",
    #         "<129>Aug 23 14:32:03 firewall auth: SSH successful login from 192.168.1.50",
    #         "<120>Aug 23 14:32:04 firewall kernel: Firewall rule triggered",
    #     ]
        
    #     with open(self.buffer_file, 'w') as f:
    #         for log in test_logs:
    #             f.write(log + '\n')
        
    #     print(f"📝 Created test log file with {len(test_logs)} entries")
    
    def load_or_generate_keys(self):
        """Load existing keys or generate new ones"""
        try:
            if os.path.exists(self.key_file) and os.path.exists(self.public_key_file):
                with open(self.key_file, 'rb') as f:
                    self.private_key = SigningKey(f.read())
                with open(self.public_key_file, 'rb') as f:
                    self.public_key = VerifyKey(f.read())
                print("✓ Loaded existing test keys")
            else:
                self.private_key = SigningKey.generate()
                self.public_key = self.private_key.verify_key
                
                with open(self.key_file, 'wb') as f:
                    f.write(self.private_key.encode())
                with open(self.public_key_file, 'wb') as f:
                    f.write(self.public_key.encode())
                
                print("✓ Generated new test keys")
                
        except Exception as e:
            print(f"❌ Key initialization failed: {e}")
            raise
    
    def create_rfc5848_structure(self, log_line: str) -> dict:
        """Create RFC 5848 inspired signed message structure"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        message_id = hashlib.sha256(f"{timestamp}{log_line}".encode()).hexdigest()[:16]
        
        # Data to be signed
        signing_data = f"{message_id}{timestamp}{log_line}".encode()
        signature = self.private_key.sign(signing_data).signature
        
        return {
            "version": "1.0",
            "message_id": message_id,
            "timestamp": timestamp,
            "original_message": log_line,
            "signature": {
                "algorithm": "ed25519",
                "key_id": self.key_id,
                "value": signature.hex()
            },
            "public_key_info": {
                "key_id": self.key_id,
                "algorithm": "ed25519",
                "public_key": self.public_key.encode().hex()
            }
        }
    
    def process_buffer(self):
        """Process the buffer file and sign logs"""
        try:
            if not os.path.exists(self.buffer_file) or os.path.getsize(self.buffer_file) == 0:
                print("ℹ️ No logs to process")
                return False
            
            signed_messages = []
            
            # Read and process logs
            with open(self.buffer_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        try:
                            signed_msg = self.create_rfc5848_structure(line)
                            signed_messages.append(signed_msg)
                            print(f"✓ Signed log {line_num}: {line[:50]}...")
                        except Exception as e:
                            print(f"⚠️ Failed to sign line {line_num}: {e}")
                            continue
            
            # Save signed messages
            if signed_messages:
                self.save_signed_batch(signed_messages)
                open(self.buffer_file, 'w').close()  # clear buffer
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Buffer processing failed: {e}")
            return False
    
    def save_signed_batch(self, messages: list):
        """Save signed messages to file"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.signed_dir, f"test_logs_{timestamp}.json")
        
        batch_data = {
            "version": "1.0",
            "batch_id": f"test_batch_{timestamp}",
            "created": datetime.utcnow().isoformat() + "Z",
            "message_count": len(messages),
            "messages": messages
        }
        
        with open(filename, 'w') as f:
            json.dump(batch_data, f, indent=2)
        
        print(f"💾 Saved {len(messages)} signed messages to {filename}")
    
    def run_test(self, cycles=3):
        """Run a test sequence"""
        print("\n" + "="*50)
        print("🧪 STARTING LOCAL TEST")
        print("="*50)
        
        for i in range(cycles):
            print(f"\n🔁 Test cycle {i+1}/{cycles}")
            print("-" * 30)
            
            success = self.process_buffer()
            if success:
                print("✅ Cycle completed successfully")
            else:
                print("⚠️ Cycle completed with issues")
            
            if i < cycles - 1:
                self.add_more_test_logs()
                time.sleep(2)
        
        print("\n" + "="*50)
        print("🏁 TEST COMPLETED")
        print("="*50)
        
        signed_files = os.listdir(self.signed_dir)
        print(f"\n📁 Generated {len(signed_files)} signed batch files:")
        for file in signed_files:
            print(f"  - {file}")
    
    def add_more_test_logs(self):
        """Add more test logs to the buffer"""
        new_logs = [
            f"<{130+i}>Aug 23 14:33:0{i} firewall test: Additional test log {i}"
            for i in range(3)
        ]
        
        with open(self.buffer_file, 'a') as f:
            for log in new_logs:
                f.write(log + '\n')
        
        print("📝 Added 3 more test logs to buffer")


if __name__ == "__main__":
    try:
        service = LocalTestSigningService()
        service.run_test(cycles=2)
        
        print("\n🎯 Next steps:")
        print("1. Check the 'signed_logs' directory for output")
        print("2. Run 'test_siem_verifier.py' to verify the signatures")
        print("3. Deploy to DigitalOcean after successful testing")
        
    except Exception as e:
        print(f"💥 Test failed: {e}")
        import traceback
        traceback.print_exc()
