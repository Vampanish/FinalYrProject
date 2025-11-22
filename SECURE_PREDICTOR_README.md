# Secure IoT Predictor - Digital Signature Integration

## Overview

This system provides **end-to-end security** for your IIoT ML pipeline with digital signatures:

1. **Input Data** → **Sign** (private key) → **Verify** (public key) → **Predict** (if valid)
2. Identifies legitimate users vs potential attackers
3. Prevents tampering with cryptographic proof

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INPUT DATA (IoT Sensor)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │  SIGN WITH PRIVATE KEY │
         │   (digital_signature)  │
         └───────────┬───────────┘
                     │
         ┌───────────▼──────────────────┐
         │ VERIFY WITH PUBLIC KEY       │
         │ Check: LEGITIMATE vs ATTACKER│
         └───────────┬──────────────────┘
                     │
        ┌────────────▼────────────┐
        │ PASS VERIFICATION?      │
        └────────────┬────────────┘
               ┌─────┴─────┐
              YES         NO
               │           │
          ┌────▼──┐    ┌──▼─────┐
          │ MODEL │    │ REJECT  │
          │ PRED  │    │ ALERT   │
          └───────┘    └─────────┘
```

---

## Files

### 1. `digital_signature.py`
**RSA-based digital signature manager**

**Features:**
- 2048-bit RSA encryption
- SHA256 hashing
- Key generation, loading, saving
- Data signing and verification

**Key Methods:**
```python
from digital_signature import DigitalSignatureManager

manager = DigitalSignatureManager()
manager.generate_keys(save=True)  # Creates private_key.pem, public_key.pem

# Sign data
signature = manager.sign_data({"user": "alice", "data": [1, 2, 3]})

# Verify data
is_valid = manager.verify_signature(data, signature)
```

---

### 2. `secure_predictor.py`
**ML model inference with signature verification**

**Features:**
- Loads `models_sample1100k` artifacts
- Full preprocessing pipeline
- Signature verification before prediction
- Single & batch predictions

**Key Methods:**
```python
from secure_predictor import SecureIoTPredictor

predictor = SecureIoTPredictor(model_dir="models_sample1100k")
predictor.setup_keys(generate_new=False)

# Single prediction
result = predictor.secure_predict(
    input_data={"F1": 0.5, "F2": 1.2, ...},  # 43 numeric features
    use_best_model="xgb"
)

print(result)
# {
#     'prediction': 0,                    # Model output
#     'probability': 0.0001,              # Confidence
#     'source': 'LEGITIMATE_USER',        # Signature verified
#     'is_valid': True,
#     'model_used': 'XGB'
# }

# Batch predictions
results = predictor.batch_secure_predict(
    input_data_list=[data1, data2, data3],
    use_best_model="xgb"
)
```

---

### 3. `demo_secure_prediction.py`
**Complete workflow demonstrations**

**Examples:**
1. **Key Generation** - Create RSA key pair
2. **Single Sample** - Sign, verify, predict one sample
3. **Batch Processing** - Process multiple samples
4. **Manual Verification** - Direct signing/verification (detect tampering)

**Run:**
```bash
python demo_secure_prediction.py
```

---

## Workflow

### Step 1: Generate RSA Key Pair
```python
from secure_predictor import SecureIoTPredictor

predictor = SecureIoTPredictor()
predictor.setup_keys(generate_new=True)
```

**Output:**
- `private_key.pem` - Keep secret (sender only)
- `public_key.pem` - Share with verifier

---

### Step 2: Prepare Input Data
Data must have **43 numeric features** (from original dataset):

```python
input_data = {
    "Mean": 0.5,
    "Sport": 1.2,
    "Dport": -0.8,
    # ... 40 more features (total 43)
}
```

---

### Step 3: Send Data
The data is **automatically signed** inside `secure_predict()`:

```python
result = predictor.secure_predict(input_data, use_best_model="xgb")
```

**Behind the scenes:**
1. Data → JSON format
2. JSON → Signed with private key
3. Signature + Data → Sent together

---

### Step 4: Receive & Verify
On receiver side:

```python
# Signature is verified using public key
if result['is_valid']:
    print(f"Prediction: {result['prediction']}")
    print(f"Source: {result['source']}")  # LEGITIMATE_USER
else:
    print(f"ALERT: Data from {result['source']}")  # POTENTIAL_ATTACKER
```

---

## Security Properties

### Authenticity
- Only sender with private key can create valid signatures
- Receiver verifies using public key

### Integrity
- Any tampering (even 1 bit) invalidates signature
- Uses SHA256 hashing + RSA-PSS padding

### Non-Repudiation
- Sender cannot deny signing the data
- Cryptographic proof exists

### Example - Tampering Detection
```python
# Original data signed by legitimate user
original_data = {"user": "alice", "timestamp": "2024-11-21"}
signature = manager.sign_data(original_data)

# Attacker modifies data
tampered_data = {"user": "bob", "timestamp": "2024-11-21"}

# Verification fails!
is_valid = manager.verify_signature(tampered_data, signature)  # False!
```

---

## Expected Output Format

### Valid Prediction (Legitimate User)
```
[OK] Signature verified. Source: LEGITIMATE_USER
Running predictions using XGB model...

Result:
  Prediction: 0
  Confidence: 0.0001
  Model: XGB
  Source: LEGITIMATE_USER
  Valid: True
```

### Invalid Signature (Attacker Detected)
```
WARNING: Source identified as POTENTIAL_ATTACKER
Result:
  prediction: None
  source: POTENTIAL_ATTACKER
  is_valid: False
```

---

## Model Selection

Use any of these models:
- `xgb` - XGBoost (recommended)
- `dt` - Decision Tree
- `knn` - K-Nearest Neighbors
- `nb` - Naive Bayes

```python
result = predictor.secure_predict(input_data, use_best_model="xgb")
```

---

## Key Files Structure

```
code/
├── digital_signature.py      # RSA signing/verification
├── secure_predictor.py       # ML + signature verification
├── demo_secure_prediction.py # Demonstrations
├── test_secure.py            # Quick test
├── models_sample1100k/        # Trained ML models
│   ├── xgb_model.pkl
│   ├── dt_model.pkl
│   ├── knn_model.pkl
│   ├── naivebayes_model.pkl
│   ├── scaler.pkl
│   └── selected_idx.npy
├── private_key.pem           # Generated (keep secret!)
└── public_key.pem            # Generated (share for verification)
```

---

## Requirements

```
cryptography>=41.0.0
scikit-learn>=1.5.0
pandas>=2.0.0
numpy>=1.24.0
xgboost>=2.0.0
```

Install:
```bash
pip install cryptography scikit-learn pandas numpy xgboost
```

---

## Use Cases

### 1. IoT Edge Device → Cloud
```
Device signs sensor data → Cloud verifies signature → Prediction
```

### 2. Real-Time Anomaly Detection
```
Stream data → Sign each batch → Verify → If tampered: ALERT
```

### 3. Multi-user System
```
Different users sign with their private keys
Server verifies using corresponding public key
Audit trail: who sent what data
```

### 4. Compliance & Audit
```
Every prediction has cryptographic proof of origin
Cannot deny or forge data sources
```

---

## Troubleshooting

**Issue: "Expected 43 numeric features, got X"**
- Solution: Ensure input dictionary has exactly 43 numeric features

**Issue: "Private key not found"**
- Solution: Run `predictor.setup_keys(generate_new=True)` first

**Issue: "Signature verification failed"**
- Solution: Data was tampered or key mismatch. Check source!

**Issue: UnicodeEncodeError in Windows**
- Solution: Already fixed! Uses plain ASCII characters

---

## Next Steps

1. ✅ Generate your keys: `predictor.setup_keys(generate_new=True)`
2. ✅ Run the demo: `python demo_secure_prediction.py`
3. ✅ Integrate into your system using examples from demo
4. ✅ Share `public_key.pem` with verifiers
5. ✅ Keep `private_key.pem` secure (consider encryption)

---

## Author
TCE Final Year Project - Secure IoT Anomaly Detection

---
