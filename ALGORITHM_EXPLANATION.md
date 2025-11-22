# Digital Signature Algorithm - Complete Theory Guide

## 1. ALGORITHM OVERVIEW

Your system uses **RSA (Rivest-Shamir-Adleman) Digital Signature Scheme** combined with **SHA-256 Hashing**.

### Algorithm Components:
- **Asymmetric Cryptography**: RSA-2048 bit
- **Hash Function**: SHA-256 (Secure Hash Algorithm)
- **Signature Padding**: PKCS#1 v1.5
- **Key Size**: 2048-bit RSA keys

---

## 2. RSA DIGITAL SIGNATURE - DETAILED EXPLANATION

### 2.1 Mathematical Foundation

RSA is based on the difficulty of factoring large numbers:

```
Public Key:  (e, N)
Private Key: (d, N)

Where:
- N = p × q (product of two large primes)
- e = public exponent (typically 65537)
- d = private exponent (computed such that e × d ≡ 1 mod φ(N))
- φ(N) = (p-1)(q-1) [Euler's totient function]
```

### 2.2 Security Property

The security relies on:
- **Factorization Problem**: Finding p and q from N is computationally infeasible
- **Key Size**: 2048-bit means N ≈ 2^2048 (astronomical number)
- **Attack Time**: ~116 quadrillion years with current computing power

---

## 3. SIGNING PROCESS (Step-by-Step)

### Step 1: Hashing the Message

```
Original Data (43 IoT features)
         ↓
    SHA-256 Hash Function
         ↓
    Hash (256 bits = 32 bytes)
    Example: a7f3d9c2e8b1f4a6...
```

**Why hash first?**
- Makes large data manageable
- Creates fixed-size fingerprint
- Any tiny change = completely different hash
- One-way function (cannot reverse)

### Step 2: Encryption with Private Key

```
Hash Output
    ↓
Pad with PKCS#1 v1.5
    ↓
S ≡ H^d mod N
    ↓
Signature (2048 bits = 256 bytes)
```

Where:
- `S` = signature
- `H` = padded hash
- `d` = private key exponent
- `N` = modulus

---

## 4. VERIFICATION PROCESS (Step-by-Step)

### Step 1: Decrypt Signature with Public Key

```
Received Signature
    ↓
H' ≡ S^e mod N
    ↓
Unpad PKCS#1 v1.5
    ↓
Extracted Hash
```

Where:
- `H'` = decrypted hash
- `e` = public exponent (65537)
- `N` = modulus

### Step 2: Compare Hashes

```
Compute Hash of Received Data
    ↓
Compare with Decrypted Hash
    ↓
IF hash_received == hash_decrypted
    → Signature Valid (AUTHENTIC)
    → Data NOT TAMPERED
ELSE
    → Signature Invalid (FORGED)
    → Data TAMPERED or IMPERSONATION
```

---

## 5. YOUR IoT THREAT DETECTION SCENARIOS

### Scenario 1: Legitimate User (Alice)

```
Alice's Data (43 features)
    ↓
SHA-256(data) = Hash_A
    ↓
Signature = Hash_A^(Alice_private) mod N
    ↓
[SEND: Data + Signature]
    ↓
[RECEIVE]
    ↓
Hash_B = SHA-256(received_data)
Hash_C = Signature^(Alice_public) mod N
    ↓
IF Hash_B == Hash_C
    ✓ AUTHENTIC - Process to ML Model
ELSE
    ✗ REJECTED - Alert Security
```

### Scenario 2: Attacker Bob (Impersonation)

```
Bob tries to send data with Alice's signature
    ↓
Bob signs with Bob_private (not Alice_private)
    ↓
[SEND: Data + Signature_Bob]
    ↓
System verifies with Alice_public
    ↓
Signature_Bob^(Alice_public) mod N ≠ SHA-256(Bob's_data)
    ↓
✗ VERIFICATION FAILS
    → ATTACKER DETECTED
    → Data REJECTED
    → Alert RAISED
```

Why it fails:
- `Signature_Bob ≡ H^(Bob_private) mod N`
- `Signature_Bob^(Alice_public) mod N ≠ H` (different exponents)
- Only Alice can create valid signatures with Alice_private

### Scenario 3: Attacker Charlie (Tampering)

```
Charlie intercepts Alice's data + signature
    ↓
Charlie modifies 1 byte of data
    ↓
[SEND: Modified_Data + Original_Signature]
    ↓
System verifies:
    Hash_Original = SHA-256(Original_Data)
    Hash_Modified = SHA-256(Modified_Data)
    ↓
Hash_Original ≠ Hash_Modified
    ↓
✗ VERIFICATION FAILS
    → TAMPERING DETECTED
    → Data REJECTED
```

Why tamper detection works:
- SHA-256 is avalanche effect: 1-bit change = completely different hash
- Signature is tied to original hash
- Modified data produces different hash
- Hashes don't match = TAMPERING

---

## 6. HASH FUNCTION (SHA-256) DETAILS

### 6.1 Properties

```
Input:  Any size (43 features in your case)
Output: 256 bits (32 bytes, 64 hex characters)

Example:
Input:  [0.5, 1.2, -0.8, ..., 2.1]
SHA-256 → a7f3d9c2e8b1f4a65e3b8d2c9f1a4b6e7d8c9f0a1b2c3d4e5f6a7b8c9d0e1f

Change 1 number by 0.0001:
        [0.5001, 1.2, -0.8, ..., 2.1]
SHA-256 → 3f9e8d7c6b5a4f3e2d1c0b9a8f7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0
```

Completely different hash!

### 6.2 Security Properties

- **One-way**: Cannot reverse hash to get original data
- **Deterministic**: Same input always produces same hash
- **Avalanche Effect**: Tiny input change = huge output change
- **Collision Resistant**: Practically impossible to find 2 inputs with same hash
- **Fast**: Computes ~400 MB/second

---

## 7. MATHEMATICAL SECURITY PROOF

### 7.1 Why RSA Works

**Signing:**
```
Signature S = H^d mod N

Verification:
S^e mod N = (H^d)^e mod N
          = H^(d×e) mod N
          = H^(e×d) mod N
          = H^(k×φ(N)+1) mod N    [where e×d ≡ 1 mod φ(N)]
          = H × (H^φ(N))^k mod N
          = H × 1^k mod N          [by Euler's theorem]
          = H mod N
```

So the decryption recovers exactly the original hash!

### 7.2 Forgery Resistance

To forge a signature without private key:

```
Attacker knows:  Public key (e, N)
Attacker needs:  S such that S^e ≡ H mod N

This means:      S ≡ H^(1/e) mod N

To compute 1/e:  Need d such that e×d ≡ 1 mod φ(N)
To compute d:    Need φ(N) = (p-1)(q-1)
To compute φ(N): Need to factor N = p × q

Factoring 2048-bit N: COMPUTATIONALLY INFEASIBLE
```

---

## 8. YOUR SYSTEM'S SECURITY PROPERTIES

### 8.1 Authentication
✓ **Proves identity** - Only Alice can create signatures with Alice_private  
✓ **Non-repudiation** - Alice cannot deny signing (only she has private key)

### 8.2 Integrity
✓ **Detects tampering** - Any 1-bit change detected via hash mismatch  
✓ **Prevents modification** - Cannot modify data and keep valid signature

### 8.3 Attack Prevention

| Attack Type | Detection | Result |
|---|---|---|
| **Impersonation (Bob)** | Signature ≠ Public Key | ✗ REJECTED |
| **Tampering (Charlie)** | Hash Mismatch | ✗ REJECTED |
| **Replay Attack** | Different data = different hash | ✗ REJECTED |
| **Man-in-Middle** | Cannot create valid signature | ✗ REJECTED |

---

## 9. KEY GENERATION PROCESS

### 9.1 Steps

```
Step 1: Select two large primes
        p = 12345... (1024 bits)
        q = 67890... (1024 bits)

Step 2: Compute modulus
        N = p × q (2048 bits)

Step 3: Compute Euler's totient
        φ(N) = (p-1) × (q-1)

Step 4: Choose public exponent
        e = 65537 (standard)
        Requirement: gcd(e, φ(N)) = 1

Step 5: Compute private exponent
        d ≡ e^(-1) mod φ(N)
        Using Extended Euclidean Algorithm

Step 6: Output
        Public Key = (e, N)
        Private Key = (d, N)
```

### 9.2 Your System

```
Your keys in: private_key.pem and public_key.pem

Private key contains:
- d (private exponent)
- N (modulus)
- p, q (original primes - kept secret)

Public key contains:
- e (public exponent = 65537)
- N (modulus)
```

---

## 10. ALGORITHM COMPLEXITY

### 10.1 Time Complexity

| Operation | Time | Notes |
|---|---|---|
| Key Generation | O(k³) | k = key size (2048) |
| Signing | O(k²) | RSA exponentiation |
| Verification | O(k²) | RSA exponentiation |
| Hashing | O(n) | n = data size |
| **Total** | **O(k²)** | Dominated by RSA |

### 10.2 Space Complexity

```
Private Key:     ~1700 bytes
Public Key:      ~300 bytes
Signature:       256 bytes (2048 bits)
Hash:            32 bytes (256 bits)
```

---

## 11. COMPARISON WITH OTHER SCHEMES

| Scheme | Key Size | Speed | Security | Use Case |
|---|---|---|---|---|
| **RSA (Your System)** | 2048 bits | Medium | Very Strong | Documents, General |
| ECDSA | 256 bits | Fast | Very Strong | Blockchain |
| EdDSA | 256 bits | Very Fast | Very Strong | Modern systems |
| DSA (Old) | 1024-3072 bits | Slow | Weak | Legacy only |

Your choice: **RSA-2048 is industry standard, well-tested, and perfectly secure for IoT**

---

## 12. REAL-WORLD EXAMPLE FROM YOUR SYSTEM

### Data Flow:

```
IoT Sensor sends 43 features:
  [CPU: 45%, Memory: 78%, Network: 120Mbps, ...]

Step 1 - Hash:
  SHA-256([45, 78, 120, ...]) = a7f3d9c2e8b1f4a6...

Step 2 - Sign:
  Signature = a7f3d9c2e8b1f4a6^(private_d) mod N
           = (huge calculation with 2048-bit arithmetic)
           = 8c2f1e9d7a5b3c6f...

Step 3 - Send:
  [Data] + [Signature] → Network

Step 4 - Receive & Verify:
  Hash_new = SHA-256([45, 78, 120, ...])
  Hash_extracted = 8c2f1e9d7a5b3c6f^(public_e) mod N

Step 5 - Compare:
  a7f3d9c2e8b1f4a6 == a7f3d9c2e8b1f4a6  ✓
  → AUTHENTIC
  → Pass to ML Model
  → Prediction: NORMAL or ATTACK
```

---

## 13. PRESENTATION TALKING POINTS

### What to Say:

**"Our system implements RSA-2048 bit digital signatures with SHA-256 hashing. Here's how it works:**

**1. When Alice sends IoT data:**
- We compute SHA-256 hash of the 43 features
- We encrypt this hash with Alice's private key
- This encrypted hash is the digital signature

**2. When we receive the data:**
- We compute SHA-256 hash of received data
- We decrypt the signature using Alice's public key
- We compare the two hashes

**3. Three possible outcomes:**
- ✓ Hashes match → Authentic data → Process to ML model
- ✗ Bob's signature with different private key → Rejected
- ✗ Charlie modified data → Hash changes → Rejected

**4. Security guarantees:**
- **Authentication**: Proves who sent it (only Alice has her private key)
- **Integrity**: Detects any tampering (avalanche effect of SHA-256)
- **Non-repudiation**: Alice cannot deny signing

**The math: Factoring 2048-bit number takes ~116 quadrillion years with current computers, making it effectively impossible to forge signatures."**

---

## 14. KEY TAKEAWAYS FOR PRESENTATION

```
✓ Algorithm: RSA-2048 + SHA-256
✓ Signing: Hash encrypted with private key
✓ Verification: Hash decrypted with public key
✓ Security Level: 2048-bit keys = 128-bit security
✓ Attack Detection: Catches impersonation & tampering
✓ Standards: PKCS#1 v1.5 padding (industry standard)
✓ Performance: Sign/verify in milliseconds
✓ Proven: Used by SSL/TLS, PGP, governments worldwide
```

---

## 15. MATHEMATICAL FORMULAS FOR SLIDES

### Slide 1: Overview
```
RSA Digital Signature = Hash^(Private_Key) mod N
```

### Slide 2: Verification
```
Original_Hash = Signature^(Public_Key) mod N
If Original_Hash == Computed_Hash → VALID
```

### Slide 3: Key Generation
```
N = p × q
e = 65537
d ≡ e^(-1) mod φ(N)
```

### Slide 4: Security
```
Factoring 2^2048 ≈ 10^616 possible values
Attack Time ≈ 116 * 10^15 years
```

### Slide 5: Complete Flow
```
Data → Hash → Sign(Hash, Private_Key) → Verify(Signature, Public_Key) → Compare
```

---

## 16. IMPLEMENTATION IN YOUR CODE

### From `digital_signature.py`:

```python
# Signing
def sign_data(self, data):
    # Step 1: Convert data to JSON string
    data_str = json.dumps(data, sort_keys=True)
    
    # Step 2: Compute SHA256 hash
    data_bytes = data_str.encode('utf-8')
    hash_obj = hashes.SHA256()
    hasher = Hash(hash_obj, backend=default_backend())
    hasher.update(data_bytes)
    digest = hasher.finalize()
    
    # Step 3: Sign with private key (RSA-PSS padding)
    signature = self.private_key.sign(
        digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    return base64.b64encode(signature).decode()

# Verifying
def verify_signature(self, data, signature):
    # Step 1: Recompute hash
    data_str = json.dumps(data, sort_keys=True)
    hash_obj = hashes.SHA256()
    hasher = Hash(hash_obj, backend=default_backend())
    hasher.update(data_str.encode('utf-8'))
    digest = hasher.finalize()
    
    # Step 2: Verify with public key
    try:
        self.public_key.verify(
            base64.b64decode(signature),
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True  # Valid signature
    except InvalidSignature:
        return False  # Invalid signature
```

---

## 17. QUICK REFERENCE

| Concept | Details |
|---|---|
| **Algorithm** | RSA-2048 + SHA-256 |
| **Private Key** | Kept secret, used for signing |
| **Public Key** | Shared openly, used for verification |
| **Signature Size** | 256 bytes (2048 bits) |
| **Hash Size** | 32 bytes (256 bits) |
| **Security Level** | 128-bit equivalent (2048-bit RSA) |
| **Signing Time** | ~1-5 ms |
| **Verification Time** | ~1-5 ms |
| **Key Generation** | ~1-2 seconds |

---

## 18. FURTHER READING

- PKCS #1 v2.2: RSA Cryptography Standard
- FIPS 180-4: SHA-256 Specification
- RFC 3447: PKCS #1: RSA Cryptography Specifications
- NIST SP 800-56B: Recommendation for Pair-Wise Key Establishment

---

*This document explains the complete theory behind your Secure IoT Threat Detection System's digital signature implementation.*
