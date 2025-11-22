import os
import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


class DigitalSignatureManager:
    def __init__(self, private_key_path=None, public_key_path=None, key_size=2048):
        self.private_key_path = private_key_path or "private_key.pem"
        self.public_key_path = public_key_path or "public_key.pem"
        self.key_size = key_size
        self.private_key = None
        self.public_key = None

    def generate_keys(self, save=True):
        print(f"Generating RSA-{self.key_size} key pair...")
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        
        if save:
            self.save_keys()
            print(f"[OK] Keys saved to {self.private_key_path} and {self.public_key_path}")
        else:
            print("[OK] Keys generated (not saved)")
        
        return self.private_key, self.public_key

    def save_keys(self):
        if self.private_key is None:
            raise RuntimeError("Private key not initialized. Call generate_keys() first.")
        
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        os.makedirs(os.path.dirname(self.private_key_path) or ".", exist_ok=True)
        os.makedirs(os.path.dirname(self.public_key_path) or ".", exist_ok=True)
        
        with open(self.private_key_path, "wb") as f:
            f.write(private_pem)
        
        with open(self.public_key_path, "wb") as f:
            f.write(public_pem)

    def load_private_key(self):
        if not os.path.exists(self.private_key_path):
            raise FileNotFoundError(f"Private key not found at {self.private_key_path}")
        
        with open(self.private_key_path, "rb") as f:
            self.private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )
        self.public_key = self.private_key.public_key()
        return self.private_key

    def load_public_key(self):
        if not os.path.exists(self.public_key_path):
            raise FileNotFoundError(f"Public key not found at {self.public_key_path}")
        
        with open(self.public_key_path, "rb") as f:
            self.public_key = serialization.load_pem_public_key(
                f.read(),
                backend=default_backend()
            )
        return self.public_key

    def sign_data(self, data):
        if self.private_key is None:
            raise RuntimeError("Private key not loaded. Call load_private_key() first.")
        
        if isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode()
        elif isinstance(data, str):
            data_bytes = data.encode()
        else:
            data_bytes = bytes(data)
        
        signature = self.private_key.sign(
            data_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        signature_b64 = base64.b64encode(signature).decode()
        return signature_b64

    def verify_signature(self, data, signature_b64):
        if self.public_key is None:
            raise RuntimeError("Public key not loaded. Call load_public_key() first.")
        
        if isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode()
        elif isinstance(data, str):
            data_bytes = data.encode()
        else:
            data_bytes = bytes(data)
        
        try:
            signature = base64.b64decode(signature_b64)
            self.public_key.verify(
                signature,
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False

    def sign_and_return(self, data):
        signature = self.sign_data(data)
        return {
            "data": data,
            "signature": signature,
            "is_valid": True
        }

    def verify_and_extract(self, signed_package):
        if "data" not in signed_package or "signature" not in signed_package:
            raise ValueError("Invalid signed package format. Expected 'data' and 'signature' keys.")
        
        data = signed_package["data"]
        signature = signed_package["signature"]
        
        is_valid = self.verify_signature(data, signature)
        
        return {
            "data": data,
            "is_valid": is_valid,
            "source": "LEGITIMATE_USER" if is_valid else "POTENTIAL_ATTACKER"
        }
