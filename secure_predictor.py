import pandas as pd
import numpy as np
import joblib
import json
import os
from digital_signature import DigitalSignatureManager

class SecureIoTPredictor:
    def __init__(self, model_dir="models_sample1100k", 
                 private_key_path="private_key.pem",
                 public_key_path="public_key.pem"):
        self.model_dir = model_dir
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path
        
        self.sig_manager = DigitalSignatureManager(private_key_path, public_key_path)
        self.models = {}
        self.scaler = None
        self.selected_idx = None
        self.selected_cols = None
        
        self._load_model_artifacts()

    def _load_model_artifacts(self):
        print(f"Loading model artifacts from '{self.model_dir}'...")
        
        try:
            self.models["knn"] = joblib.load(os.path.join(self.model_dir, "knn_model.pkl"))
            self.models["dt"] = joblib.load(os.path.join(self.model_dir, "dt_model.pkl"))
            self.models["xgb"] = joblib.load(os.path.join(self.model_dir, "xgb_model.pkl"))
            self.models["nb"] = joblib.load(os.path.join(self.model_dir, "naivebayes_model.pkl"))
            self.scaler = joblib.load(os.path.join(self.model_dir, "scaler.pkl"))
            self.selected_idx = joblib.load(os.path.join(self.model_dir, "selected_idx.npy"))
            
            if os.path.exists(os.path.join(self.model_dir, "selected_cols.pkl")):
                self.selected_cols = joblib.load(os.path.join(self.model_dir, "selected_cols.pkl"))
            
            print(f"[OK] Loaded {len(self.models)} models and preprocessing artifacts")
        except Exception as e:
            raise RuntimeError(f"Failed to load model artifacts: {e}")

    def setup_keys(self, generate_new=False):
        if generate_new or not os.path.exists(self.public_key_path):
            print("Generating new RSA key pair...")
            self.sig_manager.generate_keys(save=True)
        else:
            print("Loading existing keys...")
            self.sig_manager.load_private_key()
            self.sig_manager.load_public_key()

    def sign_input_data(self, data):
        if isinstance(data, pd.DataFrame):
            data_dict = data.to_dict(orient='records')[0] if len(data) == 1 else data.to_dict(orient='list')
        elif isinstance(data, dict):
            data_dict = data
        else:
            raise TypeError("Data must be pandas DataFrame or dict")
        
        print(f"Signing input data with private key...")
        signature = self.sig_manager.sign_data(data_dict)
        
        signed_package = {
            "data": data_dict,
            "signature": signature
        }
        
        return signed_package

    def verify_and_preprocess(self, signed_package):
        print("Verifying digital signature...")
        result = self.sig_manager.verify_and_extract(signed_package)
        
        if not result["is_valid"]:
            print(f"⚠ WARNING: Source identified as {result['source']}")
            return None, result
        
        print(f"[OK] Signature verified. Source: {result['source']}")
        
        data = result["data"]
        
        if isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            df = pd.DataFrame(data)
        
        df = df.select_dtypes(include=[np.number]).copy()
        df = df.fillna(df.median())
        
        if df.shape[1] < 43:
            raise ValueError(f"Expected 43 numeric features, got {df.shape[1]}")
        
        X_scaled_full = self.scaler.transform(df.values)
        
        if self.selected_idx is not None and len(self.selected_idx) > 0:
            X_selected = X_scaled_full[:, self.selected_idx]
        else:
            X_selected = X_scaled_full
        
        return X_selected, result

    def predict(self, X_scaled, use_best_model="xgb"):
        print(f"\nRunning predictions using {use_best_model.upper()} model...")
        
        model = self.models[use_best_model]
        prediction = model.predict(X_scaled)
        proba = model.predict_proba(X_scaled) if hasattr(model, "predict_proba") else None
        
        return prediction, proba

    def secure_predict(self, input_data, use_best_model="xgb"):
        try:
            signed_package = self.sign_input_data(input_data)
            
            X_scaled, verify_result = self.verify_and_preprocess(signed_package)
            
            if X_scaled is None:
                return {
                    "prediction": None,
                    "probability": None,
                    "source": verify_result["source"],
                    "is_valid": False
                }
            
            prediction, proba = self.predict(X_scaled, use_best_model)
            
            return {
                "prediction": int(prediction[0]),
                "probability": float(proba[0][1]) if proba is not None else None,
                "source": verify_result["source"],
                "is_valid": True,
                "model_used": use_best_model.upper()
            }
        
        except Exception as e:
            return {
                "prediction": None,
                "probability": None,
                "error": str(e),
                "is_valid": False
            }

    def batch_secure_predict(self, input_data_list, use_best_model="xgb"):
        results = []
        for idx, data in enumerate(input_data_list):
            print(f"\nProcessing sample {idx+1}/{len(input_data_list)}...")
            result = self.secure_predict(data, use_best_model)
            results.append(result)
        
        return results
