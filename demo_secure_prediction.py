import pandas as pd
import numpy as np
from secure_predictor import SecureIoTPredictor

def example_1_key_generation():
    print("="*70)
    print("EXAMPLE 1: Generate RSA Key Pair")
    print("="*70)
    
    predictor = SecureIoTPredictor()
    predictor.setup_keys(generate_new=True)
    
    print(f"\n[OK] Keys ready for signing and verification\n")


def example_2_single_sample_prediction():
    print("="*70)
    print("EXAMPLE 2: Single Sample with Digital Signature Verification")
    print("="*70)
    
    predictor = SecureIoTPredictor()
    predictor.setup_keys(generate_new=False)
    
    sample_data = {
        "Mean": 0.5, "Sport": 1.2, "Dport": -0.8, "SrcPkts": 2.1, "DstPkts": 0.3,
        "TotPkts": 1.0, "DstBytes": 0.2, "SrcBytes": -0.5, "TotBytes": 1.5, "SrcLoad": 0.8,
        "DstLoad": -0.3, "Rate": 0.1, "Duration": 2.0, "Idle": -1.0, "F1": 0.5,
        "F2": 1.2, "F3": -0.8, "F4": 2.1, "F5": 0.3, "F6": 1.0,
        "F7": 0.2, "F8": -0.5, "F9": 1.5, "F10": 0.8, "F11": -0.3,
        "F12": 0.1, "F13": 2.0, "F14": -1.0, "F15": 0.5, "F16": 1.2,
        "F17": -0.8, "F18": 2.1, "F19": 0.3, "F20": 1.0, "F21": 0.2,
        "F22": -0.5, "F23": 1.5, "F24": 0.8, "F25": -0.3, "F26": 0.1,
        "F27": 2.0, "F28": -1.0, "F29": 0.5
    }
    
    print(f"\nInput data: {len(sample_data)} features provided\n")
    
    result = predictor.secure_predict(sample_data, use_best_model="xgb")
    
    print(f"\nResult:")
    if result['is_valid']:
        print(f"  Prediction: {result['prediction']}")
        print(f"  Confidence: {result['probability']:.4f}" if result['probability'] else "  N/A")
        print(f"  Model: {result.get('model_used', 'N/A')}")
    else:
        print(f"  Error: {result.get('error', 'Unknown error')}")
    print(f"  Source: {result.get('source', 'Unknown')}")
    print(f"  Valid: {result['is_valid']}\n")


def example_3_batch_prediction():
    print("="*70)
    print("EXAMPLE 3: Batch Prediction with Signature Verification")
    print("="*70)
    
    predictor = SecureIoTPredictor()
    predictor.setup_keys(generate_new=False)
    
    batch_data = [
        {
            "Mean": 0.5, "Sport": 1.2, "Dport": -0.8, "SrcPkts": 2.1, "DstPkts": 0.3,
            "TotPkts": 1.0, "DstBytes": 0.2, "SrcBytes": -0.5, "TotBytes": 1.5, "SrcLoad": 0.8,
            "DstLoad": -0.3, "Rate": 0.1, "Duration": 2.0, "Idle": -1.0, "F1": 0.5,
            "F2": 1.2, "F3": -0.8, "F4": 2.1, "F5": 0.3, "F6": 1.0,
            "F7": 0.2, "F8": -0.5, "F9": 1.5, "F10": 0.8, "F11": -0.3,
            "F12": 0.1, "F13": 2.0, "F14": -1.0, "F15": 0.5, "F16": 1.2,
            "F17": -0.8, "F18": 2.1, "F19": 0.3, "F20": 1.0, "F21": 0.2,
            "F22": -0.5, "F23": 1.5, "F24": 0.8, "F25": -0.3, "F26": 0.1,
            "F27": 2.0, "F28": -1.0, "F29": 0.5
        },
        {
            "Mean": 1.0, "Sport": 2.0, "Dport": 0.0, "SrcPkts": 1.5, "DstPkts": -0.5,
            "TotPkts": 0.5, "DstBytes": 1.0, "SrcBytes": 0.3, "TotBytes": 0.7, "SrcLoad": 1.2,
            "DstLoad": 0.4, "Rate": 0.5, "Duration": 1.5, "Idle": -0.5, "F1": 1.0,
            "F2": 2.0, "F3": 0.0, "F4": 1.5, "F5": -0.5, "F6": 0.5,
            "F7": 1.0, "F8": 0.3, "F9": 0.7, "F10": 1.2, "F11": 0.4,
            "F12": 0.5, "F13": 1.5, "F14": -0.5, "F15": 1.0, "F16": 2.0,
            "F17": 0.0, "F18": 1.5, "F19": -0.5, "F20": 0.5, "F21": 1.0,
            "F22": 0.3, "F23": 0.7, "F24": 1.2, "F25": 0.4, "F26": 0.5,
            "F27": 1.5, "F28": -0.5, "F29": 1.0
        },
        {
            "Mean": -0.5, "Sport": 0.5, "Dport": 1.0, "SrcPkts": -1.0, "DstPkts": 1.5,
            "TotPkts": 0.2, "DstBytes": 0.8, "SrcBytes": 1.3, "TotBytes": 0.5, "SrcLoad": 0.3,
            "DstLoad": 1.1, "Rate": 0.9, "Duration": 0.4, "Idle": 1.2, "F1": -0.5,
            "F2": 0.5, "F3": 1.0, "F4": -1.0, "F5": 1.5, "F6": 0.2,
            "F7": 0.8, "F8": 1.3, "F9": 0.5, "F10": 0.3, "F11": 1.1,
            "F12": 0.9, "F13": 0.4, "F14": 1.2, "F15": -0.5, "F16": 0.5,
            "F17": 1.0, "F18": -1.0, "F19": 1.5, "F20": 0.2, "F21": 0.8,
            "F22": 1.3, "F23": 0.5, "F24": 0.3, "F25": 1.1, "F26": 0.9,
            "F27": 0.4, "F28": 1.2, "F29": -0.5
        },
    ]
    
    results = predictor.batch_secure_predict(batch_data, use_best_model="xgb")
    
    print(f"\n{'='*70}")
    print("BATCH RESULTS SUMMARY")
    print(f"{'='*70}")
    for idx, result in enumerate(results, 1):
        print(f"\nSample {idx}:")
        if result['is_valid']:
            print(f"  Prediction: {result['prediction']}")
            print(f"  Confidence: {result['probability']:.4f}" if result['probability'] else "  N/A")
        else:
            print(f"  Error: {result.get('error', 'Unknown error')}")
        print(f"  Source: {result.get('source', 'Unknown')}")
        print(f"  Valid: {result['is_valid']}")


def example_4_manual_signing_verification():
    print("="*70)
    print("EXAMPLE 4: Manual Sign & Verify (Advanced)")
    print("="*70)
    
    from digital_signature import DigitalSignatureManager
    
    sig_manager = DigitalSignatureManager()
    
    sig_manager.load_private_key()
    sig_manager.load_public_key()
    
    test_data = {"user_id": "user_123", "timestamp": "2024-11-21", "data": [1, 2, 3]}
    
    print(f"\nOriginal data: {test_data}")
    
    signature = sig_manager.sign_data(test_data)
    print(f"\nSignature (first 50 chars): {signature[:50]}...")
    
    is_valid = sig_manager.verify_signature(test_data, signature)
    print(f"Verification result: {is_valid}")
    
    tampered_data = {"user_id": "attacker_456", "timestamp": "2024-11-21", "data": [1, 2, 3]}
    is_valid_tampered = sig_manager.verify_signature(tampered_data, signature)
    print(f"\nTampered data verification: {is_valid_tampered}")
    print("(This should be False, indicating tampering detected)\n")


if __name__ == "__main__":
    print("\n")
    print("=" * 70)
    print("SECURE IoT PREDICTOR - DEMO GUIDE".center(70))
    print("=" * 70)
    
    print("\nWORKFLOW:")
    print("  1. Generate RSA key pair (private_key.pem, public_key.pem)")
    print("  2. Input data is signed with private key")
    print("  3. Signature is verified with public key")
    print("  4. Only verified data enters the ML model")
    print("  5. Source is identified as LEGITIMATE_USER or POTENTIAL_ATTACKER")
    
    print("\n\n[Running Example 1]")
    example_1_key_generation()
    
    print("\n\n[Running Example 2]")
    example_2_single_sample_prediction()
    
    print("\n\n[Running Example 3]")
    example_3_batch_prediction()
    
    print("\n\n[Running Example 4]")
    example_4_manual_signing_verification()
    
    print("\n" + "="*70)
    print("USAGE IN YOUR CODE:")
    print("="*70)
    print("""
from secure_predictor import SecureIoTPredictor

predictor = SecureIoTPredictor(model_dir="models_sample1100k")
predictor.setup_keys(generate_new=False)

input_data = {"Feature1": 0.5, "Feature2": 1.2, ...}
result = predictor.secure_predict(input_data, use_best_model="xgb")

print(f"Prediction: {result['prediction']}")
print(f"Source: {result['source']}")
print(f"Valid: {result['is_valid']}")
    """)
    print("="*70 + "\n")
