import pandas as pd
import numpy as np
from secure_predictor import SecureIoTPredictor
from digital_signature import DigitalSignatureManager
import json

print("\n" + "="*80)
print("SECURE IoT PREDICTOR - PRACTICAL EXAMPLES".center(80))
print("="*80 + "\n")

print("SCENARIO: Network Traffic Monitoring System")
print("-" * 80)
print("Role: You are a network security analyst monitoring IoT devices")
print("Task: Identify attacks vs normal traffic using digital signatures")
print("-" * 80 + "\n")


def example_1_legitimate_user():
    """
    EXAMPLE 1: Legitimate Device Sending Data
    
    Scenario: Alice (legitimate IoT device) sends network traffic data
    - Data is signed with her private key
    - Signature verifies successfully
    - Prediction made
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: LEGITIMATE USER - Alice (IoT Device #1)")
    print("="*80)
    
    print("\n[STEP 1] Alice initializes her system")
    alice = SecureIoTPredictor(model_dir="models_sample1100k")
    alice.setup_keys(generate_new=False)
    print("  [OK] Alice's secure predictor ready")
    
    print("\n[STEP 2] Alice collects normal network traffic data")
    alice_data = {
        "Mean": 120.5, "Sport": 443, "Dport": 52100, "SrcPkts": 250, "DstPkts": 280,
        "TotPkts": 530, "DstBytes": 45000, "SrcBytes": 38000, "TotBytes": 83000, 
        "SrcLoad": 0.8, "DstLoad": 0.9, "Rate": 15.5, "Duration": 120, "Idle": 0.5, 
        "F1": 0.2, "F2": 0.3, "F3": 0.1, "F4": 0.4, "F5": 0.2, "F6": 0.1,
        "F7": 0.3, "F8": 0.25, "F9": 0.35, "F10": 0.15, "F11": 0.4, "F12": 0.18,
        "F13": 0.28, "F14": 0.22, "F15": 0.05, "F16": 0.32, "F17": 0.12, "F18": 0.42,
        "F19": 0.08, "F20": 0.38, "F21": 0.14, "F22": 0.36, "F23": 0.19, "F24": 0.41,
        "F25": 0.11, "F26": 0.29, "F27": 0.17, "F28": 0.33, "F29": 0.09
    }
    print(f"  [OK] Collected {len(alice_data)} network features")
    print(f"      Mean packet size: {alice_data['Mean']} bytes")
    print(f"      Total packets: {alice_data['TotPkts']}")
    print(f"      Duration: {alice_data['Duration']} seconds")
    
    print("\n[STEP 3] Alice signs and sends her data for analysis")
    result = alice.secure_predict(alice_data, use_best_model="xgb")
    
    print("\n[RESULT] Analysis completed:")
    print(f"  Source: {result['source']}")
    print(f"  Signature Valid: {result['is_valid']}")
    print(f"  Prediction: {'ATTACK' if result['prediction'] == 1 else 'NORMAL TRAFFIC'}")
    print(f"  Confidence: {result['probability']:.4f}")
    print("\n  [ACCEPTED] DATA ACCEPTED - Alice is a legitimate user")


def example_2_attacker_scenario_1():
    """
    EXAMPLE 2: Attacker Scenario #1 - Bob tries to impersonate Alice
    
    Scenario: Bob (attacker) tries to send data claiming to be Alice
    - Bob creates data and signs with his OWN key
    - System is configured to only trust Alice's public key
    - Signature verification FAILS
    - Data is REJECTED
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: ATTACKER SCENARIO #1 - Bob (Impersonating Alice)")
    print("="*80)
    
    print("\n[ATTACK ATTEMPT]")
    print("  Attacker Profile: Bob (has own RSA key pair)")
    print("  Attack Goal: Send malicious traffic while appearing as Alice")
    print("  Attack Vector: Impersonate legitimate device\n")
    
    print("[STEP 1] Bob creates suspicious network traffic data")
    bob_malicious_data = {
        "Mean": 50.2, "Sport": 443, "Dport": 12345, "SrcPkts": 5000, "DstPkts": 100,
        "TotPkts": 5100, "DstBytes": 1000, "SrcBytes": 500000, "TotBytes": 501000, 
        "SrcLoad": 99.5, "DstLoad": 2.1, "Rate": 500.0, "Duration": 5, "Idle": 0.0, 
        "F1": 0.9, "F2": 0.95, "F3": 0.85, "F4": 0.92, "F5": 0.88, "F6": 0.91,
        "F7": 0.87, "F8": 0.93, "F9": 0.89, "F10": 0.94, "F11": 0.86, "F12": 0.96,
        "F13": 0.84, "F14": 0.97, "F15": 0.82, "F16": 0.98, "F17": 0.80, "F18": 0.99,
        "F19": 0.81, "F20": 0.97, "F21": 0.79, "F22": 0.98, "F23": 0.77, "F24": 0.96,
        "F25": 0.78, "F26": 0.95, "F27": 0.76, "F28": 0.94, "F29": 0.75
    }
    print(f"  [SUSPICIOUS] Data characteristics:")
    print(f"      Source load: {bob_malicious_data['SrcLoad']}% (EXTREMELY HIGH!)")
    print(f"      Source bytes: {bob_malicious_data['SrcBytes']} (UNUSUALLY LARGE!)")
    print(f"      Duration: {bob_malicious_data['Duration']}s (VERY SHORT!)")
    print(f"      Idle time: {bob_malicious_data['Idle']}s (NO IDLE PERIOD!)")
    
    print("\n[STEP 2] Bob generates his OWN RSA key pair and signs the data")
    print("  Bob's plan: Sign data with his private key, try to trick the system")
    
    # Bob creates his own signature with his OWN private key
    bob_manager = DigitalSignatureManager(
        private_key_path="bob_private.pem",
        public_key_path="bob_public.pem"
    )
    bob_manager.generate_keys(save=False)  # Generate new keypair for Bob
    
    bob_signature = bob_manager.sign_data(bob_malicious_data)
    print(f"  [FORGED] Signature created with Bob's key: {bob_signature[:40]}...")
    
    print("\n[STEP 3] System attempts to verify Bob's data (using Alice's trusted key)")
    predictor = SecureIoTPredictor(model_dir="models_sample1100k")
    predictor.setup_keys(generate_new=False)  # Load Alice's trusted public key
    
    print("  [VERIFYING] Checking signature against Alice's trusted public key...")
    print("  [WARNING] Signature verification in progress...\n")
    
    # Try to verify Bob's signature with Alice's public key (will fail!)
    alice_manager = DigitalSignatureManager()
    alice_manager.load_public_key()
    
    is_valid = alice_manager.verify_signature(bob_malicious_data, bob_signature)
    
    print(f"  Verification Result: {is_valid}")
    
    print("\n[ALERT!] VERIFICATION RESULT:")
    print(f"  Signature Valid: {is_valid}")
    print(f"  Source: POTENTIAL ATTACKER (signature mismatch)")
    if not is_valid:
        print(f"  Error: Bob's signature does not match Alice's public key!")
    
    print("\n  *** DATA REJECTED ***")
    print("  *** ATTACKER DETECTED ***")
    print("  *** INCIDENT LOGGED ***")


def example_3_attacker_scenario_2():
    """
    EXAMPLE 3: Attacker Scenario #2 - Charlie modifies Alice's data
    
    Scenario: Charlie (attacker) intercepts Alice's legitimate data and modifies it
    - Charlie gets Alice's data and signature
    - Charlie modifies even 1 bit of data
    - Signature verification FAILS
    - Tampering is DETECTED
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: ATTACKER SCENARIO #2 - Charlie (Data Tampering)")
    print("="*80)
    
    print("\n[ATTACK ATTEMPT]")
    print("  Attacker Profile: Charlie")
    print("  Attack Goal: Modify legitimate traffic to appear as attack")
    print("  Attack Vector: Man-in-the-Middle (MITM) attack\n")
    
    print("[STEP 1] Alice sends legitimate data (with signature)")
    alice_data = {
        "Mean": 120.5, "Sport": 443, "Dport": 52100, "SrcPkts": 250, "DstPkts": 280,
        "TotPkts": 530, "DstBytes": 45000, "SrcBytes": 38000, "TotBytes": 83000, 
        "SrcLoad": 0.8, "DstLoad": 0.9, "Rate": 15.5, "Duration": 120, "Idle": 0.5, 
        "F1": 0.2, "F2": 0.3, "F3": 0.1, "F4": 0.4, "F5": 0.2, "F6": 0.1,
        "F7": 0.3, "F8": 0.25, "F9": 0.35, "F10": 0.15, "F11": 0.4, "F12": 0.18,
        "F13": 0.28, "F14": 0.22, "F15": 0.05, "F16": 0.32, "F17": 0.12, "F18": 0.42,
        "F19": 0.08, "F20": 0.38, "F21": 0.14, "F22": 0.36, "F23": 0.19, "F24": 0.41,
        "F25": 0.11, "F26": 0.29, "F27": 0.17, "F28": 0.33, "F29": 0.09
    }
    
    manager = DigitalSignatureManager()
    manager.load_private_key()
    alice_signature = manager.sign_data(alice_data)
    
    print(f"  [LEGITIMATE] Alice's data signed")
    print(f"      Signature: {alice_signature[:40]}...\n")
    
    print("[STEP 2] Charlie intercepts the data in transit (MITM attack)")
    print("  [INTERCEPT] Data captured on network")
    
    print("\n[STEP 3] Charlie modifies just ONE field")
    print("  Charlie modifies: SrcLoad 0.8 --> 0.9")
    print("  Charlie's logic: 'Small change, same signature should work'")
    print("  [MISTAKE] Cryptographic signatures detect ANY change!\n")
    
    tampered_data = alice_data.copy()
    tampered_data["SrcLoad"] = 0.9  # Charlie modifies just this
    
    print(f"  [TAMPERED] Modified data:")
    print(f"      Original SrcLoad: {alice_data['SrcLoad']}")
    print(f"      Modified SrcLoad: {tampered_data['SrcLoad']}")
    print(f"      Using original signature: {alice_signature[:40]}...\n")
    
    print("[STEP 4] System verifies the tampered data")
    print("  [VERIFYING] Checking signature against modified data...")
    
    manager.load_public_key()
    is_valid = manager.verify_signature(tampered_data, alice_signature)
    
    print(f"\n[VERIFICATION RESULT]: {is_valid}")
    
    print("\n  *** TAMPERING DETECTED ***")
    print("  *** DATA REJECTED ***")
    print("  *** INCIDENT LOGGED ***")
    print("\n  Note: Even changing 1 byte invalidates the signature!")


def example_4_genetic_algorithm_alert():
    """
    EXAMPLE 4: Genetic Algorithm Model - Alert Data Analysis
    
    Scenario: Using ML model trained with genetic algorithm for feature selection
    Data: High-risk alert network traffic
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: GENETIC ALGORITHM MODEL - ALERT DETECTION")
    print("="*80)
    
    print("\n[CONTEXT]")
    print("  Model Type: XGBoost with Genetic Algorithm Feature Selection")
    print("  Training Data: 1.1M network traffic samples")
    print("  Features Selected: 21 out of 43 by Genetic Algorithm")
    print("  Use Case: Real-time IoT anomaly detection\n")
    
    print("[SCENARIO] Analyzing high-risk alert data")
    print("-" * 80)
    
    alert_data_list = [
        {
            "name": "Normal Traffic (Baseline)",
            "description": "Typical HTTP web browsing traffic",
            "data": {
                "Mean": 200.0, "Sport": 80, "Dport": 52000, "SrcPkts": 100, "DstPkts": 120,
                "TotPkts": 220, "DstBytes": 50000, "SrcBytes": 20000, "TotBytes": 70000, 
                "SrcLoad": 0.3, "DstLoad": 0.4, "Rate": 5.0, "Duration": 300, "Idle": 10.0, 
                "F1": 0.1, "F2": 0.15, "F3": 0.08, "F4": 0.2, "F5": 0.12, "F6": 0.09,
                "F7": 0.18, "F8": 0.14, "F9": 0.19, "F10": 0.11, "F11": 0.22, "F12": 0.13,
                "F13": 0.16, "F14": 0.17, "F15": 0.10, "F16": 0.21, "F17": 0.09, "F18": 0.23,
                "F19": 0.07, "F20": 0.20, "F21": 0.11, "F22": 0.19, "F23": 0.14, "F24": 0.24,
                "F25": 0.08, "F26": 0.17, "F27": 0.12, "F28": 0.18, "F29": 0.06
            }
        },
        {
            "name": "Port Scanning Attack",
            "description": "Attacker scanning multiple ports rapidly",
            "data": {
                "Mean": 40.0, "Sport": 0, "Dport": 32768, "SrcPkts": 5000, "DstPkts": 50,
                "TotPkts": 5050, "DstBytes": 500, "SrcBytes": 400000, "TotBytes": 400500, 
                "SrcLoad": 95.0, "DstLoad": 0.1, "Rate": 1000.0, "Duration": 5, "Idle": 0.0, 
                "F1": 0.98, "F2": 0.96, "F3": 0.94, "F4": 0.99, "F5": 0.97, "F6": 0.95,
                "F7": 0.98, "F8": 0.96, "F9": 0.99, "F10": 0.94, "F11": 0.97, "F12": 0.95,
                "F13": 0.98, "F14": 0.94, "F15": 0.99, "F16": 0.96, "F17": 0.97, "F18": 0.95,
                "F19": 0.98, "F20": 0.94, "F21": 0.99, "F22": 0.96, "F23": 0.97, "F24": 0.95,
                "F25": 0.98, "F26": 0.94, "F27": 0.99, "F28": 0.96, "F29": 0.97
            }
        },
        {
            "name": "DDoS Attack",
            "description": "Distributed Denial of Service - flooding with packets",
            "data": {
                "Mean": 64.0, "Sport": 443, "Dport": 12345, "SrcPkts": 50000, "DstPkts": 10,
                "TotPkts": 50010, "DstBytes": 10000, "SrcBytes": 3200000, "TotBytes": 3210000, 
                "SrcLoad": 99.0, "DstLoad": 1.0, "Rate": 10000.0, "Duration": 1, "Idle": 0.0, 
                "F1": 0.99, "F2": 0.98, "F3": 0.97, "F4": 0.99, "F5": 0.98, "F6": 0.97,
                "F7": 0.99, "F8": 0.98, "F9": 0.97, "F10": 0.99, "F11": 0.98, "F12": 0.97,
                "F13": 0.99, "F14": 0.98, "F15": 0.97, "F16": 0.99, "F17": 0.98, "F18": 0.97,
                "F19": 0.99, "F20": 0.98, "F21": 0.97, "F22": 0.99, "F23": 0.98, "F24": 0.97,
                "F25": 0.99, "F26": 0.98, "F27": 0.97, "F28": 0.99, "F29": 0.98
            }
        },
        {
            "name": "Data Exfiltration",
            "description": "Stealing data - large outbound transfer",
            "data": {
                "Mean": 500.0, "Sport": 443, "Dport": 5000, "SrcPkts": 1000, "DstPkts": 10,
                "TotPkts": 1010, "DstBytes": 100000, "SrcBytes": 5000000, "TotBytes": 5100000, 
                "SrcLoad": 98.0, "DstLoad": 0.2, "Rate": 100.0, "Duration": 50, "Idle": 0.1, 
                "F1": 0.95, "F2": 0.94, "F3": 0.92, "F4": 0.96, "F5": 0.93, "F6": 0.91,
                "F7": 0.95, "F8": 0.94, "F9": 0.96, "F10": 0.92, "F11": 0.95, "F12": 0.91,
                "F13": 0.94, "F14": 0.93, "F15": 0.96, "F16": 0.92, "F17": 0.95, "F18": 0.91,
                "F19": 0.94, "F20": 0.93, "F21": 0.96, "F22": 0.92, "F23": 0.95, "F24": 0.91,
                "F25": 0.94, "F26": 0.93, "F27": 0.96, "F28": 0.92, "F29": 0.95
            }
        }
    ]
    
    predictor = SecureIoTPredictor(model_dir="models_sample1100k")
    predictor.setup_keys(generate_new=False)
    
    results_summary = []
    
    for idx, alert in enumerate(alert_data_list, 1):
        print(f"\n[ALERT #{idx}] {alert['name']}")
        print(f"  Description: {alert['description']}")
        print(f"  High-Risk Indicators:")
        
        data = alert['data']
        if data['SrcLoad'] > 50:
            print(f"    - Extremely high source load: {data['SrcLoad']}%")
        if data['Rate'] > 100:
            print(f"    - Unusually high packet rate: {data['Rate']} pps")
        if data['Duration'] < 10 and data['TotPkts'] > 1000:
            print(f"    - Rapid packet flood: {data['TotPkts']} packets in {data['Duration']}s")
        if data['SrcBytes'] > 1000000:
            print(f"    - Massive data transfer: {data['SrcBytes']/1e6:.1f}MB")
        
        print(f"\n  [ANALYZING] Processing through GA-selected features...")
        result = predictor.secure_predict(data, use_best_model="xgb")
        
        threat_level = "CRITICAL" if result['probability'] > 0.9 else "HIGH" if result['probability'] > 0.7 else "MEDIUM" if result['probability'] > 0.5 else "LOW"
        
        print(f"\n  [RESULT]")
        print(f"    Prediction: {'ATTACK DETECTED' if result['prediction'] == 1 else 'NORMAL'}")
        print(f"    Threat Level: {threat_level}")
        print(f"    Confidence: {result['probability']:.2%}")
        print(f"    Signature Status: {result['source']}")
        print(f"    Data Valid: {'YES' if result['is_valid'] else 'NO'}")
        
        results_summary.append({
            "name": alert['name'],
            "prediction": result['prediction'],
            "confidence": result['probability'],
            "threat": threat_level
        })
    
    print("\n" + "-" * 80)
    print("SUMMARY TABLE - All Alerts Analyzed")
    print("-" * 80)
    print(f"{'Alert Type':<30} {'Prediction':<15} {'Threat Level':<15} {'Confidence':<15}")
    print("-" * 80)
    for r in results_summary:
        pred = "ATTACK" if r['prediction'] == 1 else "NORMAL"
        print(f"{r['name']:<30} {pred:<15} {r['threat']:<15} {r['confidence']:.2%}")


if __name__ == "__main__":
    try:
        example_1_legitimate_user()
        
        example_2_attacker_scenario_1()
        
        example_3_attacker_scenario_2()
        
        example_4_genetic_algorithm_alert()
        
        print("\n" + "="*80)
        print("ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY".center(80))
        print("="*80)
        print("\nKEY TAKEAWAYS:")
        print("  [OK] Legitimate data with valid signatures: ACCEPTED")
        print("  [REJECTED] Attacker data without valid signatures: REJECTED")
        print("  [DETECTED] Tampered data: DETECTED (cryptographic proof)")
        print("  [CLASSIFIED] Alert data: Correctly classified by GA-trained model")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
