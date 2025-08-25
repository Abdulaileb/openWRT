# #!/usr/bin/env python3
# import json
# import os
# import glob
# import base64
# from datetime import datetime

# # Use PyNaCl instead of ed25519
# import nacl.signing
# import nacl.encoding

# # Local test configuration
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# LOCAL_SIGNED_DIR = os.path.join(BASE_DIR, "signed_logs")
# LOCAL_KEY_DIR = os.path.join(BASE_DIR, "keys")
# TEST_PUBLIC_KEY_FILE = os.path.join(LOCAL_KEY_DIR, "test_signing.pub")

# class LocalSIEMVerifier:
#     def __init__(self):
#         self.verify_key = None
#         self.load_public_key()
    
#     def load_public_key(self):
#         """Load public key from local test file using PyNaCl"""
#         try:
#             with open(TEST_PUBLIC_KEY_FILE, 'rb') as f:
#                 key_data = f.read()
#                 self.verify_key = nacl.signing.VerifyKey(key_data)
#             print("✓ Loaded test public key successfully")
#             return True
#         except Exception as e:
#             print(f"❌ Failed to load public key: {e}")
#             return False
    
#     def verify_message(self, signed_message: dict) -> dict:
#         """Verify a single signed message using PyNaCl"""
#         try:
#             if not self.verify_key:
#                 return {"valid": False, "error": "No public key available"}
            
#             # Check required fields
#             required_fields = ['message_id', 'timestamp', 'original_message', 'signature']
#             for field in required_fields:
#                 if field not in signed_message:
#                     return {"valid": False, "error": f"Missing field: {field}"}
            
#             if 'value' not in signed_message['signature']:
#                 return {"valid": False, "error": "Missing signature value"}
            
#             # Recreate signing data
#             signing_data = f"{signed_message['message_id']}{signed_message['timestamp']}{signed_message['original_message']}".encode()
            
#             # Verify signature using PyNaCl
#             signature_bytes = base64.b64decode(signed_message['signature']['value'])
#             self.verify_key.verify(signing_data, signature_bytes)
            
#             return {"valid": True, "message": "Signature verified successfully"}
            
#         except nacl.exceptions.BadSignatureError:
#             return {"valid": False, "error": "Invalid signature - possible tampering"}
#         except Exception as e:
#             return {"valid": False, "error": f"Verification failed: {str(e)}"}
    
#     def test_verification(self):
#         """Test verification with the latest signed batch"""
#         # Find the most recent signed file
#         signed_files = glob.glob(os.path.join(LOCAL_SIGNED_DIR, "*.json"))
#         if not signed_files:
#             print("❌ No signed files found. Run test_signing_service.py first.")
#             return
        
#         latest_file = max(signed_files, key=os.path.getctime)
#         print(f"🔍 Testing verification of: {os.path.basename(latest_file)}")
        
#         try:
#             with open(latest_file, 'r') as f:
#                 batch_data = json.load(f)
            
#             if 'messages' not in batch_data:
#                 print("❌ Invalid batch file format")
#                 return
            
#             print(f"📊 Found {len(batch_data['messages'])} messages to verify")
            
#             results = {"valid": 0, "invalid": 0, "errors": []}
            
#             for i, message in enumerate(batch_data['messages']):
#                 result = self.verify_message(message)
                
#                 if result['valid']:
#                     results['valid'] += 1
#                     print(f"✓ Message {i+1}: Valid")
#                 else:
#                     results['invalid'] += 1
#                     error_msg = f"Message {i+1}: {result['error']}"
#                     results['errors'].append(error_msg)
#                     print(f"❌ {error_msg}")
            
#             print(f"\n🎯 Verification Results:")
#             print(f"   Valid: {results['valid']}")
#             print(f"   Invalid: {results['invalid']}")
#             print(f"   Success Rate: {results['valid']/(results['valid']+results['invalid'])*100:.1f}%")
            
#             if results['invalid'] > 0:
#                 print(f"\n⚠️  {results['invalid']} messages failed verification!")
#                 for error in results['errors'][:3]:
#                     print(f"   - {error}")
            
#             # Test tampering detection
#             if batch_data['messages']:
#                 self.test_tampering_detection(batch_data['messages'][0])
            
#         except Exception as e:
#             print(f"❌ Failed to process batch file: {e}")
    
#     def test_tampering_detection(self, original_message: dict):
#         """Test that tampering is detected"""
#         print(f"\n🔒 Testing tampering detection...")
        
#         # Create a tampered message
#         tampered_message = original_message.copy()
#         tampered_message['original_message'] += " TAMPERED!"
        
#         result = self.verify_message(tampered_message)
        
#         if not result['valid'] and "tampering" in result['error'].lower():
#             print("✓ Tampering correctly detected!")
#         else:
#             print("❌ Tampering detection failed!")
#             print(f"   Expected: Invalid signature due to tampering")
#             print(f"   Got: {result}")

# if __name__ == "__main__":
#     print("🔐 Local SIEM Verifier Test")
#     print("=" * 40)
    
#     # Check if PyNaCl is installed
#     try:
#         import nacl.signing
#     except ImportError:
#         print("📦 Installing PyNaCl library...")
#         import subprocess
#         subprocess.check_call(["pip", "install", "pynacl"])
#         import nacl.signing
    
#     verifier = LocalSIEMVerifier()
    
#     if verifier.verify_key:
#         verifier.test_verification()
        
#         print(f"\n🎯 Test completed!")
#         print("Next: Deploy these scripts to DigitalOcean after successful testing")
#     else:
#         print("❌ Cannot proceed without public key")
#         print("Please run test_signing_service.py first to generate keys")



#!/usr/bin/env python3
import json
import os
import glob
from config.test_config import *

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


class LocalSIEMVerifier:
    def __init__(self):
        self.public_key = None
        self.load_public_key()
    
    def load_public_key(self):
        """Load public key from local test file"""
        try:
            with open(TEST_PUBLIC_KEY_FILE, 'rb') as f:
                key_data = f.read()
                self.public_key = VerifyKey(key_data)
            print("✓ Loaded test public key successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to load public key: {e}")
            return False
    
    def verify_message(self, signed_message: dict) -> dict:
        """Verify a single signed message"""
        try:
            if not self.public_key:
                return {"valid": False, "error": "No public key available"}
            
            # Check required fields
            required_fields = ['message_id', 'timestamp', 'original_message', 'signature']
            for field in required_fields:
                if field not in signed_message:
                    return {"valid": False, "error": f"Missing field: {field}"}
            
            if 'value' not in signed_message['signature']:
                return {"valid": False, "error": "Missing signature value"}
            
            # Recreate signing data (must match signer)
            signing_data = f"{signed_message['message_id']}{signed_message['timestamp']}{signed_message['original_message']}".encode()
            
            # Verify signature
            signature_bytes = bytes.fromhex(signed_message['signature']['value'])
            self.public_key.verify(signing_data, signature_bytes)
            
            return {"valid": True, "message": "Signature verified successfully"}
            
        except BadSignatureError:
            return {"valid": False, "error": "Invalid signature - possible tampering"}
        except Exception as e:
            return {"valid": False, "error": f"Verification failed: {str(e)}"}
    
    def test_verification(self):
        """Test verification with the latest signed batch"""
        # Find the most recent signed file
        signed_files = glob.glob(os.path.join(LOCAL_SIGNED_DIR, "*.json"))
        if not signed_files:
            print("❌ No signed files found. Run test_signing_service.py first.")
            return
        
        latest_file = max(signed_files, key=os.path.getctime)
        print(f"🔍 Testing verification of: {os.path.basename(latest_file)}")
        
        try:
            with open(latest_file, 'r') as f:
                batch_data = json.load(f)
            
            if 'messages' not in batch_data:
                print("❌ Invalid batch file format")
                return
            
            print(f"📊 Found {len(batch_data['messages'])} messages to verify")
            
            results = {"valid": 0, "invalid": 0, "errors": []}
            
            for i, message in enumerate(batch_data['messages']):
                result = self.verify_message(message)
                
                if result['valid']:
                    results['valid'] += 1
                    print(f"✓ Message {i+1}: Valid")
                else:
                    results['invalid'] += 1
                    error_msg = f"Message {i+1}: {result['error']}"
                    results['errors'].append(error_msg)
                    print(f"❌ {error_msg}")
            
            print(f"\n🎯 Verification Results:")
            print(f"   Valid: {results['valid']}")
            print(f"   Invalid: {results['invalid']}")
            print(f"   Success Rate: {results['valid']/(results['valid']+results['invalid'])*100:.1f}%")
            
            if results['invalid'] > 0:
                print(f"\n⚠️  {results['invalid']} messages failed verification!")
                for error in results['errors'][:3]:
                    print(f"   - {error}")
            
            # Test tampering detection
            self.test_tampering_detection(batch_data['messages'][0])
            
        except Exception as e:
            print(f"❌ Failed to process batch file: {e}")
    
    def test_tampering_detection(self, original_message: dict):
        """Test that tampering is detected"""
        print(f"\n🔒 Testing tampering detection...")
        
        # Create a tampered message
        tampered_message = original_message.copy()
        tampered_message['original_message'] += " TAMPERED!"
        
        result = self.verify_message(tampered_message)
        
        if not result['valid'] and "tampering" in result['error'].lower():
            print("✓ Tampering correctly detected!")
        else:
            print("❌ Tampering detection failed!")
            print(f"   Expected: Invalid signature due to tampering")
            print(f"   Got: {result}")


if __name__ == "__main__":
    print("🔐 Local SIEM Verifier Test")
    print("=" * 40)
    
    verifier = LocalSIEMVerifier()
    
    if verifier.public_key:
        verifier.test_verification()
        
        print(f"\n🎯 Test completed!")
        print("Next: Deploy these scripts to DigitalOcean after successful testing")
    else:
        print("❌ Cannot proceed without public key")
        print("Please run test_signing_service.py first to generate keys")
