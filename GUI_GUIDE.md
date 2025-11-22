# Secure IoT GUI - User Guide

## 🎨 Interface Overview

The Secure IoT Threat Detection System provides a professional, color-coded GUI interface with 4 interactive scenarios.

### **Left Panel - Control Buttons**

```
📋 SCENARIOS
├─ ✓ Original User (Alice - Legitimate)    [GREEN]
├─ ⚠ Attacker #1 (Bob - Impersonation)     [RED]
├─ ⚠ Attacker #2 (Charlie - Tampering)     [RED]
└─ 📊 Alert Analysis (Multiple Threats)    [YELLOW]

📈 DATA SETTINGS
├─ Threat Intensity: [Normal / Moderate / Severe]
└─ 🗑️ Clear Display
```

### **Right Panel - Output Tabs**

```
📊 Process Flow      → Shows step-by-step execution
🔍 Data Details      → IoT sensor readings (43 features)
🎯 Prediction Results → ML model output & confidence
🔐 Security Analysis → Authentication & integrity checks
```

---

## 🎯 Scenario Walkthrough

### **Scenario 1: Original User (Alice)**

**What Happens:**
1. ✓ Generates 43 legitimate sensor features
2. 🔏 Signs data with Alice's PRIVATE key (RSA 2048-bit)
3. ✅ Verifies signature with Alice's PUBLIC key
4. 🤖 Runs XGBoost model (21 GA-selected features)
5. ✓ Produces prediction: NORMAL TRAFFIC

**Expected Output:**
```
SCENARIO 1: LEGITIMATE USER (ALICE)

[STEP 1] 📊 Generate IoT Sensor Data
✓ Generated 43 sensor features
  Mean Load: 2.45%
  Total Packets: 850

[STEP 2] 🔏 Digital Signature Creation
  Using: RSA 2048-bit + SHA256 hash
✓ Data signed successfully
  Signature: dXJNFTsOiFc2/zH/pv8Iq8233k4...
  Signature length: 256 bytes

[STEP 3] ✅ Signature Verification
  Verifying with Alice's PUBLIC key
✓ Signature verification: VALID
  Data integrity: ✓ CONFIRMED

[STEP 4] 🤖 ML Model Prediction
  Feature selection: Genetic Algorithm (21/43 features)
  Running XGBoost model...

Prediction Class: NORMAL
Confidence: 4.51%
Model Used: XGBoost
Data Valid: True

[STEP 5] 📋 Final Verdict
✓ TRANSACTION COMPLETED SUCCESSFULLY
```

---

### **Scenario 2: Attacker - Impersonation (Bob)**

**What Happens:**
1. 👹 Bob generates malicious data (high load, many packets)
2. 🔓 Bob signs with his OWN RSA key (NOT Alice's)
3. ❌ Verification FAILS because Bob's key ≠ Alice's key
4. 🛑 Data is REJECTED before ML prediction
5. 🚨 ATTACKER DETECTED

**Expected Output:**
```
SCENARIO 2: ATTACKER - IMPERSONATION ATTEMPT (BOB)

[STEP 1] 👹 Attacker Generates Malicious Data
⚠ Suspicious patterns detected
  High load: 75.23%
  Excessive packets: 15000

[STEP 2] 🔓 Attacker Signs with OWN RSA Key
  ⚠ Critical Problem: Bob's key ≠ Alice's key
✓ Bob's signature created: Up8coZcWcQ0ngw94brXprac...

[STEP 3] ❌ Signature Verification FAILS
  System verifying with Alice's PUBLIC key
✗ Signature verification: INVALID
  Reason: Bob's signature ≠ Alice's public key

[STEP 4] 🛑 Data REJECTED - No Model Execution
  System halted before prediction phase
  Reason: Signature verification failed

[STEP 5] 🚨 SECURITY ALERT
  Source: Bob (Attacker - Impersonation)
  Signature Valid: ✗ NO
  Verdict: REJECTED - ATTACKER DETECTED

✗ TRANSACTION BLOCKED - SECURITY BREACH DETECTED
```

---

### **Scenario 3: Attacker - Data Tampering (Charlie)**

**What Happens:**
1. ✓ Alice creates & signs legitimate data
2. 🔏 Signature is created with SHA256 hash
3. 👹 Charlie intercepts, modifies ONE field (e.g., SrcLoad: 0.8 → 0.9)
4. 🔍 Verification detects tampering (hash no longer matches)
5. ✗ Data is REJECTED due to integrity violation

**Expected Output:**
```
SCENARIO 3: ATTACKER - DATA TAMPERING (CHARLIE)

[STEP 1] ✓ Alice Creates Legitimate Data
✓ All values in normal range

[STEP 2] 🔏 Alice Signs Data with Private Key
✓ Signature: dXJNFTsOiFc2/zH/pv8Iq8233k4...
  SHA256 Hash Created: 185f8db32271fe25...

[STEP 3] 👹 Charlie INTERCEPTS & MODIFIES Data
  ⚠ Man-in-the-middle attack detected!
  Modified field: SrcLoad
    Original:  0.8000
    Tampered:  1.3000
  Change: Only 62.50% of one field
  Signature kept: UNCHANGED (original from Alice)

[STEP 4] 🔍 Tamper Detection - Verification FAILS
  Computing SHA256 hash of tampered data...
✗ Hash verification: NO MATCH
  Result: Single byte modification = completely different hash
  Conclusion: DATA TAMPERING DETECTED

[STEP 5] 🚨 TAMPERING ALERT - DATA REJECTED
  Source: Charlie (Attacker - Tampering)
  Signature Valid: ✗ NO
  Data Tampered: ✗ YES
  Verdict: REJECTED - TAMPERING DETECTED

✗ TRANSACTION BLOCKED - DATA INTEGRITY COMPROMISED
```

---

### **Scenario 4: Alert Analysis**

**What Happens:**
1. Processes 4 different alert types
2. Each goes through complete pipeline (sign → verify → predict)
3. Shows threat levels (LOW, MEDIUM, HIGH, CRITICAL)
4. All have valid signatures (from Alice)
5. Displays predictions for each

**Expected Output:**
```
SCENARIO 4: ALERT ANALYSIS - MULTIPLE THREAT TYPES

[ALERT 1] Normal Traffic
────────────────────────────────────
  Type: Legitimate IoT Traffic
  Signature: ✓ VALID
  Prediction: 0
  Confidence: 8.75%
  Threat Level: LOW

[ALERT 2] Port Scanning Attack
────────────────────────────────────
  Type: Port Scanning Attack
  Signature: ✓ VALID
  Prediction: 0
  Confidence: 5.13%
  Threat Level: MEDIUM

[ALERT 3] DDoS Attack
────────────────────────────────────
  Type: DDoS Attack
  Signature: ✓ VALID
  Prediction: 0
  Confidence: 5.13%
  Threat Level: HIGH

[ALERT 4] Data Exfiltration
────────────────────────────────────
  Type: Data Exfiltration
  Signature: ✓ VALID
  Prediction: 0
  Confidence: 4.51%
  Threat Level: CRITICAL

📊 ANALYSIS SUMMARY
════════════════════════════════════
  Total Alerts Processed: 4
  All Signatures: Valid ✓
  Threat Distribution:
    • Normal Traffic: LOW
    • Port Scanning Attack: MEDIUM
    • DDoS Attack: HIGH
    • Data Exfiltration: CRITICAL
```

---

## 🎮 How to Use the GUI

### **Step 1: Launch the Application**
```bash
cd "E:\Final Yr Project\code"
python secure_iot_ui.py
```

### **Step 2: Wait for System Initialization**
- The left panel shows "Status: Initializing..."
- System loads:
  - ML models (4 models from models_sample1100k)
  - Alice's RSA keys (alice_private.pem, alice_public.pem)
  - Bob's RSA keys (bob_private.pem, bob_public.pem)
  - Charlie's RSA keys (charlie_private.pem, charlie_public.pem)
- Once ready: "Status: Ready" ✓

### **Step 3: Click a Scenario Button**

| Button | Purpose | Expected Result |
|--------|---------|-----------------|
| ✓ Original User | Show legitimate data flow | ✓ ACCEPTED |
| ⚠ Attacker #1 | Show impersonation failure | ✗ REJECTED (signature mismatch) |
| ⚠ Attacker #2 | Show tampering detection | ✗ REJECTED (data modified) |
| 📊 Alert Analysis | Process multiple alerts | All verified, predictions made |

### **Step 4: Select Threat Intensity (Optional)**
- **Normal**: Regular IoT traffic patterns
- **Moderate**: Suspicious but moderate attack indicators
- **Severe**: Extreme attack patterns (high load, many packets)

### **Step 5: View Results**
- **Process Flow tab**: See step-by-step execution
- **Data Details tab**: Raw sensor values (43 features)
- **Prediction Results tab**: ML output & confidence
- **Security Analysis tab**: Authentication & integrity status

### **Step 6: Clear Display**
- Click "🗑️ Clear Display" to reset all panels
- Run another scenario

---

## 🔐 Security Features Demonstrated

### **Scenario 1 (Legitimate User)**
✓ **Valid Signature** - Data comes from Alice (proven with RSA)
✓ **Integrity Confirmed** - SHA256 hash matches
✓ **Model Executes** - Prediction made normally
✓ **Status**: ACCEPTED

### **Scenario 2 (Impersonation)**
✗ **Invalid Signature** - Bob's key ≠ Alice's key
✗ **Authenticity Failed** - Cannot prove data is from Alice
✗ **No Model Execution** - System blocks before prediction
✗ **Status**: REJECTED

### **Scenario 3 (Tampering)**
✗ **Hash Mismatch** - Even 1-byte change invalidates entire hash
✗ **Integrity Failed** - Data was modified after signing
✗ **No Model Execution** - Verification catches tampering
✗ **Status**: REJECTED

### **Scenario 4 (Alert Analysis)**
✓ **All Valid Signatures** - All data from Alice
✓ **Predictions Made** - ML runs on all alerts
⚠ **Threat Levels Shown** - LOW/MEDIUM/HIGH/CRITICAL
✓ **Status**: ACCEPTED (with threat classification)

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────┐
│ USER CLICKS SCENARIO BUTTON                             │
└────────────────────┬────────────────────────────────────┘
                     ↓
        ┌────────────────────────────┐
        │ Generate IoT Data (43 Feat) │
        └────────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │ Sign with RSA + SHA256      │ ← Alice/Bob/Charlie key
        └────────────┬───────────────┘
                     ↓
        ┌────────────────────────────┐
        │ Verify Signature           │ ← Alice's public key
        └────────────┬───────────────┘
                     ↓
           ┌─────────┴────────┐
           │                  │
        [VALID]            [INVALID]
           │                  │
           ↓                  ↓
    ┌────────────────┐   ┌──────────────┐
    │ Preprocess     │   │ REJECT DATA  │
    │ Scale Data     │   │ LOG ALERT    │
    └────────┬───────┘   │ RETURN ERROR │
             ↓            └──────────────┘
    ┌────────────────┐
    │ GA Select 21   │
    │ Features       │
    └────────┬───────┘
             ↓
    ┌────────────────┐
    │ Run ML Model   │
    │ (XGBoost)      │
    └────────┬───────┘
             ↓
    ┌────────────────┐
    │ Get Prediction │
    │ + Confidence   │
    └────────┬───────┘
             ↓
    ┌────────────────────┐
    │ Display Results    │
    │ ✓ ACCEPTED        │
    └────────────────────┘
```

---

## 🎨 Color Coding

| Color | Meaning | Examples |
|-------|---------|----------|
| 🟢 **GREEN** | Success / Legitimate | ✓ Valid Signature, Alice data |
| 🔴 **RED** | Error / Attacker | ✗ Failed Signature, Bob/Charlie |
| 🟡 **YELLOW** | Warning / Alert | ⚠ Suspicious patterns |
| 🔵 **BLUE** | Process / Info | Process steps, feature info |

---

## 📁 Files Created/Used

```
secure_iot_ui.py              ← Main GUI application
digital_signature.py          ← RSA cryptography engine
secure_predictor.py           ← ML integration layer
models_sample1100k/           ← Trained ML models
  ├─ model_comparison.csv
  ├─ selected_idx.npy        ← GA selected features (21)
  ├─ X_test.csv
  └─ y_test.csv
*_private.pem                 ← Private keys (Alice, Bob, Charlie)
*_public.pem                  ← Public keys (Alice, Bob, Charlie)
```

---

## 🚀 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Scroll in tabs | View more output |
| Close window | Exit application |

---

## ⚡ Performance

- **Initialization**: ~2-3 seconds (loading models)
- **Per scenario**: ~1-2 seconds (sign + verify + predict)
- **Network data**: 43 IoT features per sample
- **Model speed**: XGBoost + 21 GA-selected features (fast)

---

## 🐛 Troubleshooting

### **GUI Won't Launch**
```bash
# Check if tkinter is installed
python -m tkinter
# If error, install: pip install tk
```

### **Models Not Found**
- Ensure `models_sample1100k/` directory exists
- Check file paths in `secure_predictor.py`

### **Sklearn Warnings**
- These are expected (version mismatch)
- Does not affect functionality
- To fix: `pip install scikit-learn==1.7.2`

### **RSA Keys Not Found**
- System auto-generates keys on first run
- Check for `*_private.pem` and `*_public.pem` files
- If not created, check file permissions

---

## 📈 Next Steps

1. **Monitor Attacks**: Click different attacker scenarios to see real-time detection
2. **Analyze Alerts**: Use Alert Analysis to see multiple threat types
3. **Adjust Settings**: Change threat intensity to see data variations
4. **Export Results**: Copy output from tabs for documentation
5. **Deploy**: Use as production monitoring interface

---

## ✅ System Checklist

Before running:
- [ ] Python 3.8+
- [ ] Required libraries: tkinter, cryptography, pandas, numpy, sklearn
- [ ] Models folder: `models_sample1100k/`
- [ ] Dataset: `wustl_iiot_2021.csv`
- [ ] Modules: `digital_signature.py`, `secure_predictor.py`

---

## 🎓 Educational Value

This GUI demonstrates:
- ✓ RSA 2048-bit digital signatures
- ✓ SHA256 cryptographic hashing
- ✓ Attacker detection methods
- ✓ Tampering detection via integrity checks
- ✓ Machine learning integration
- ✓ Genetic algorithm feature selection
- ✓ Real-time IoT threat analysis
- ✓ Professional UI/UX design

Perfect for teaching cybersecurity, cryptography, and IoT security concepts!
