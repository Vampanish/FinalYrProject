# Quick Start Guide - Secure IoT Predictor

## 30-Second Setup

```python
from secure_predictor import SecureIoTPredictor

# 1. Initialize
predictor = SecureIoTPredictor(model_dir="models_sample1100k")

# 2. Generate keys (first time only)
predictor.setup_keys(generate_new=True)

# 3. Make prediction with signature verification
input_data = {f'F{i}': 0.5 for i in range(43)}  # 43 features
result = predictor.secure_predict(input_data, use_best_model="xgb")

# 4. Check result
print(f"Prediction: {result['prediction']}")           # 0 or 1
print(f"Is Valid:   {result['is_valid']}")            # True or False
print(f"Source:     {result['source']}")              # LEGITIMATE_USER or POTENTIAL_ATTACKER
```

---

## Input Data Format

**Must provide exactly 43 numeric features:**

```python
input_data = {
    "Mean": value1,
    "Sport": value2,
    "Dport": value3,
    # ... (40 more features from your dataset)
}
```

Or programmatically:
```python
import pandas as pd

# Load from CSV
df = pd.read_csv("sample.csv")
data_dict = df.iloc[0].to_dict()

result = predictor.secure_predict(data_dict)
```

---

## Return Values

```python
result = {
    'prediction': int,                    # 0 or 1 (attack or normal)
    'probability': float,                 # Confidence 0.0-1.0
    'source': str,                        # LEGITIMATE_USER or POTENTIAL_ATTACKER
    'is_valid': bool,                     # True = signature verified
    'model_used': str,                    # XGB, DT, KNN, or NB
    'error': str                          # (if any)
}
```

---

## Models Available

```python
# All return same interface
predictor.secure_predict(data, use_best_model="xgb")    # XGBoost
predictor.secure_predict(data, use_best_model="dt")     # Decision Tree
predictor.secure_predict(data, use_best_model="knn")    # K-Nearest Neighbors
predictor.secure_predict(data, use_best_model="nb")     # Naive Bayes
```

---

## Batch Processing

```python
data_list = [data1, data2, data3]
results = predictor.batch_secure_predict(data_list, use_best_model="xgb")

# results is a list of dictionaries
for idx, result in enumerate(results):
    print(f"Sample {idx}: {result['prediction']} - {result['source']}")
```

---

## Key Management

### First Time (Generate Keys)
```python
predictor.setup_keys(generate_new=True)
# Creates: private_key.pem, public_key.pem
```

### Subsequent Times (Load Keys)
```python
predictor.setup_keys(generate_new=False)
# Loads existing keys
```

### Manual Key Setup
```python
from digital_signature import DigitalSignatureManager

manager = DigitalSignatureManager(
    private_key_path="my_private.pem",
    public_key_path="my_public.pem"
)

manager.generate_keys(save=True)  # Create fresh keys
# or
manager.load_private_key()         # Load existing
manager.load_public_key()
```

---

## Direct Signing (Advanced)

```python
from digital_signature import DigitalSignatureManager

manager = DigitalSignatureManager()
manager.load_private_key()

# Sign data
data = {"user": "alice", "action": "login"}
signature = manager.sign_data(data)

# Verify (you or someone with public key)
manager.load_public_key()
is_valid = manager.verify_signature(data, signature)  # True

# Try tampering
tampered = {"user": "bob", "action": "login"}
is_valid = manager.verify_signature(tampered, signature)  # False!
```

---

## Common Workflows

### Workflow 1: Single Real-Time Prediction
```python
from secure_predictor import SecureIoTPredictor

predictor = SecureIoTPredictor()
predictor.setup_keys(generate_new=False)

# Get sensor data from IoT device
sensor_data = read_sensor()  # Returns dict with 43 features

# Predict with verification
result = predictor.secure_predict(sensor_data)

if result['is_valid']:
    if result['prediction'] == 1:
        alert("ATTACK DETECTED!")
    else:
        log("Normal traffic")
else:
    alert(f"SOURCE: {result['source']}")
```

### Workflow 2: Batch Processing
```python
# Read multiple samples
samples = pd.read_csv("network_traffic.csv")

# Convert to list of dicts
data_list = [row.to_dict() for _, row in samples.iterrows()]

# Process all with signatures
results = predictor.batch_secure_predict(data_list)

# Analyze
for i, result in enumerate(results):
    source = "✓ LEGIT" if result['is_valid'] else "⚠ ATTACK"
    print(f"Sample {i}: {result['prediction']} - {source}")
```

### Workflow 3: User Authentication
```python
# Different users have different keys
users = {
    "alice": {"private": "alice_private.pem", "public": "alice_public.pem"},
    "bob": {"private": "bob_private.pem", "public": "bob_public.pem"}
}

def process_user_data(username, data):
    manager = DigitalSignatureManager(
        users[username]["private"],
        users[username]["public"]
    )
    manager.load_private_key()
    manager.load_public_key()
    
    # Verify this user sent the data
    if manager.verify_signature(data, data["signature"]):
        print(f"Data authenticated from {username}")
        return predictor.secure_predict(data)
    else:
        print(f"FAKE DATA: someone impersonating {username}")
```

---

## Error Handling

```python
result = predictor.secure_predict(input_data)

if result['is_valid']:
    # Good signature, proceed with prediction
    prediction = result['prediction']
    confidence = result['probability']
else:
    # Signature invalid - reject immediately
    error_msg = result.get('error', 'Unknown error')
    source = result.get('source', 'Unknown')
    
    if source == 'POTENTIAL_ATTACKER':
        # Log security event
        log_security_alert(error_msg)
    else:
        # Data format error
        log_error(error_msg)
```

---

## Performance Notes

- **Key Generation**: ~1-2 seconds (one-time)
- **Signing**: <100ms per sample
- **Verification**: <100ms per sample
- **Model Prediction**: 10-500ms depending on model
- **Total per sample**: 100-600ms

---

## Security Notes

⚠️ **Important:**
- **Never share `private_key.pem`** - it's your signing key
- **Share `public_key.pem`** - others use it to verify your signatures
- Store private key securely (consider encrypting with password)
- Use SSH to transmit keys between systems

✓ **What you get:**
- Cryptographic proof of data origin
- Detection of any tampering
- Non-repudiation (sender can't deny)
- Audit trail with digital signatures

---

## Files Reference

| File | Purpose | Create? | Share? |
|------|---------|---------|---------|
| `private_key.pem` | Signing key | Once | Never |
| `public_key.pem` | Verification key | Once | Always |
| `models_sample1100k/` | ML models | Pre-trained | Optional |
| `digital_signature.py` | Crypto module | Pre-built | Share |
| `secure_predictor.py` | Main API | Pre-built | Share |

---

## Testing

```bash
# Quick test
python test_secure.py

# Full demo with all examples
python demo_secure_prediction.py

# Run manually
python
>>> from secure_predictor import SecureIoTPredictor
>>> p = SecureIoTPredictor()
>>> p.setup_keys(generate_new=False)
>>> data = {f'F{i}': 0.5 for i in range(43)}
>>> r = p.secure_predict(data)
>>> print(r)
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `Expected 43 features, got X` | Wrong data size | Add/remove features |
| `Private key not found` | Never generated | Call `setup_keys(generate_new=True)` |
| `Signature verification failed` | Data tampered | Check source field |
| `X has Y features` | Scaler mismatch | Ensure 43 numeric features |
| `FileNotFoundError` | Keys missing | Generate keys first |

---

## Next: Integration

1. Copy `digital_signature.py` and `secure_predictor.py` to your project
2. Run `demo_secure_prediction.py` to verify setup
3. Use `SecureIoTPredictor` in your application
4. Deploy `public_key.pem` to verification endpoints
5. Keep `private_key.pem` secure on sending endpoint

---

Questions? See `SECURE_PREDICTOR_README.md` for details.
