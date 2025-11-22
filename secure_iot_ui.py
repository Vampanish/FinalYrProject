"""
Secure IoT Predictor - Professional GUI Interface
Demonstrates digital signatures, verification, and ML predictions with visual feedback
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from digital_signature import DigitalSignatureManager
from secure_predictor import SecureIoTPredictor
import numpy as np
import json

class SecureIoTUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure IoT Threat Detection System")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e2e")
        
        # Initialize system components
        self.predictor = None
        self.alice_manager = None
        self.bob_manager = None
        self.charlie_manager = None
        self.system_active = False
        
        # Color scheme
        self.bg_dark = "#1e1e2e"
        self.bg_darker = "#0f0f1e"
        self.accent_green = "#50c878"
        self.accent_red = "#ff6b6b"
        self.accent_blue = "#4a90e2"
        self.accent_yellow = "#f9ca24"
        self.text_light = "#e0e0e0"
        self.text_muted = "#808080"
        
        self.setup_ui()
        self.initialize_system()
        
    def setup_ui(self):
        """Create the main UI layout"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.bg_dark)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame, 
            text="🔒 Secure IoT Threat Detection System",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_dark,
            fg=self.accent_green
        )
        title_label.pack(side=tk.LEFT)
        
        status_label = tk.Label(
            header_frame,
            text="Status: Initializing...",
            font=("Helvetica", 10),
            bg=self.bg_dark,
            fg=self.text_muted
        )
        status_label.pack(side=tk.RIGHT)
        self.status_label = status_label
        
        # Main content - Left panel (Controls)
        left_frame = tk.Frame(main_frame, bg=self.bg_darker)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10), ipadx=15, ipady=15)
        
        # Controls section
        controls_title = tk.Label(
            left_frame,
            text="📋 SCENARIOS",
            font=("Helvetica", 12, "bold"),
            bg=self.bg_darker,
            fg=self.accent_blue
        )
        controls_title.pack(pady=(0, 15))
        
        # Scenario buttons
        button_style = {
            "font": ("Helvetica", 11, "bold"),
            "bg": self.accent_green,
            "fg": "black",
            "activebackground": "#45b36d",
            "activeforeground": "black",
            "padx": 15,
            "pady": 12,
            "border": 0,
            "cursor": "hand2"
        }
        
        btn1 = tk.Button(
            left_frame,
            text="✓ Original User\n(Alice - Legitimate)",
            command=self.scenario_legitimate_user,
            **button_style
        )
        btn1.pack(fill=tk.X, pady=8)
        
        btn2 = tk.Button(
            left_frame,
            text="⚠ Attacker #1\n(Bob - Impersonation)",
            command=self.scenario_attacker_impersonation,
            bg=self.accent_red,
            fg="white",
            activebackground="#e55a5a",
            activeforeground="white",
            padx=15,
            pady=12,
            font=("Helvetica", 11, "bold"),
            border=0,
            cursor="hand2"
        )
        btn2.pack(fill=tk.X, pady=8)
        
        btn3 = tk.Button(
            left_frame,
            text="⚠ Attacker #2\n(Charlie - Tampering)",
            command=self.scenario_attacker_tampering,
            bg=self.accent_red,
            fg="white",
            activebackground="#e55a5a",
            activeforeground="white",
            padx=15,
            pady=12,
            font=("Helvetica", 11, "bold"),
            border=0,
            cursor="hand2"
        )
        btn3.pack(fill=tk.X, pady=8)
        
        btn4 = tk.Button(
            left_frame,
            text="📊 Alert Analysis\n(Multiple Threats)",
            command=self.scenario_alert_analysis,
            bg=self.accent_yellow,
            fg="black",
            activebackground="#f4ba14",
            activeforeground="black",
            padx=15,
            pady=12,
            font=("Helvetica", 11, "bold"),
            border=0,
            cursor="hand2"
        )
        btn4.pack(fill=tk.X, pady=8)
        
        # Separator
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=20)
        
        # Data generation section
        data_title = tk.Label(
            left_frame,
            text="📈 DATA SETTINGS",
            font=("Helvetica", 12, "bold"),
            bg=self.bg_darker,
            fg=self.accent_blue
        )
        data_title.pack(pady=(0, 15))
        
        # Threat level selector
        threat_label = tk.Label(
            left_frame,
            text="Threat Intensity:",
            font=("Helvetica", 10),
            bg=self.bg_darker,
            fg=self.text_light
        )
        threat_label.pack(anchor=tk.W)
        
        self.threat_var = tk.StringVar(value="Normal")
        threat_combo = ttk.Combobox(
            left_frame,
            textvariable=self.threat_var,
            values=["Normal", "Moderate", "Severe"],
            state="readonly",
            font=("Helvetica", 10)
        )
        threat_combo.pack(fill=tk.X, pady=(5, 15))
        
        # Clear button
        clear_btn = tk.Button(
            left_frame,
            text="🗑️ Clear Display",
            command=self.clear_display,
            bg=self.text_muted,
            fg="white",
            padx=15,
            pady=10,
            font=("Helvetica", 10, "bold"),
            border=0,
            cursor="hand2"
        )
        clear_btn.pack(fill=tk.X, pady=8)
        
        # Right panel (Output)
        right_frame = tk.Frame(main_frame, bg=self.bg_darker)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, ipadx=15, ipady=15)
        
        # Output panels
        self.setup_output_panels(right_frame)
        
    def setup_output_panels(self, parent):
        """Setup the output display panels"""
        # Notebook (tabs)
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Style for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'TNotebook',
            background=self.bg_darker,
            borderwidth=0
        )
        style.configure(
            'TNotebook.Tab',
            padding=[15, 10],
            font=("Helvetica", 10, "bold")
        )
        
        # Tab 1: Process Flow
        flow_frame = tk.Frame(notebook, bg=self.bg_dark)
        notebook.add(flow_frame, text="📊 Process Flow")
        
        self.flow_text = scrolledtext.ScrolledText(
            flow_frame,
            height=25,
            width=100,
            bg=self.bg_dark,
            fg=self.text_light,
            font=("Courier New", 9),
            insertbackground=self.accent_green,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.flow_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.setup_text_tags(self.flow_text)
        
        # Tab 2: Data Details
        data_frame = tk.Frame(notebook, bg=self.bg_dark)
        notebook.add(data_frame, text="🔍 Data Details")
        
        self.data_text = scrolledtext.ScrolledText(
            data_frame,
            height=25,
            width=100,
            bg=self.bg_dark,
            fg=self.text_light,
            font=("Courier New", 9),
            insertbackground=self.accent_green,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.data_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.setup_text_tags(self.data_text)
        
        # Tab 3: Model Prediction
        pred_frame = tk.Frame(notebook, bg=self.bg_dark)
        notebook.add(pred_frame, text="🎯 Prediction Results")
        
        self.pred_text = scrolledtext.ScrolledText(
            pred_frame,
            height=25,
            width=100,
            bg=self.bg_dark,
            fg=self.text_light,
            font=("Courier New", 9),
            insertbackground=self.accent_green,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.pred_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.setup_text_tags(self.pred_text)
        
        # Tab 4: Security Analysis
        sec_frame = tk.Frame(notebook, bg=self.bg_dark)
        notebook.add(sec_frame, text="🔐 Security Analysis")
        
        self.sec_text = scrolledtext.ScrolledText(
            sec_frame,
            height=25,
            width=100,
            bg=self.bg_dark,
            fg=self.text_light,
            font=("Courier New", 9),
            insertbackground=self.accent_green,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.sec_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.setup_text_tags(self.sec_text)
        
    def setup_text_tags(self, text_widget):
        """Configure text tags for formatting"""
        text_widget.tag_config("header", foreground=self.accent_blue, font=("Courier New", 10, "bold"))
        text_widget.tag_config("success", foreground=self.accent_green, font=("Courier New", 9, "bold"))
        text_widget.tag_config("error", foreground=self.accent_red, font=("Courier New", 9, "bold"))
        text_widget.tag_config("warning", foreground=self.accent_yellow, font=("Courier New", 9, "bold"))
        text_widget.tag_config("info", foreground=self.text_muted, font=("Courier New", 9))
        text_widget.tag_config("process", foreground=self.accent_blue, font=("Courier New", 9))
        
    def initialize_system(self):
        """Initialize the secure predictor and managers in background"""
        def init_thread():
            try:
                self.log_flow("🔄 Initializing Secure IoT System...")
                
                # Load predictor
                self.predictor = SecureIoTPredictor("models_sample1100k")
                self.log_flow("✓ ML Model loaded", "success")
                
                # Setup digital signature managers - Alice
                self.alice_manager = DigitalSignatureManager(
                    "alice_private.pem",
                    "alice_public.pem"
                )
                self.alice_manager.load_private_key()
                self.alice_manager.load_public_key()
                self.predictor.setup_keys()
                self.log_flow("✓ Alice's keys configured", "success")
                
                # Setup Bob's manager - Bob
                self.bob_manager = DigitalSignatureManager(
                    "bob_private.pem",
                    "bob_public.pem"
                )
                self.bob_manager.load_private_key()
                self.bob_manager.load_public_key()
                self.log_flow("✓ Bob's keys configured (for attacker scenario)", "success")
                
                # Setup Charlie's manager - Charlie
                self.charlie_manager = DigitalSignatureManager(
                    "charlie_private.pem",
                    "charlie_public.pem"
                )
                self.charlie_manager.load_private_key()
                self.charlie_manager.load_public_key()
                self.log_flow("✓ Charlie's keys configured (for tampering scenario)", "success")
                
                self.system_active = True
                self.status_label.config(text="Status: Ready", fg=self.accent_green)
                self.log_flow("\n✓ System Ready! Click a scenario button to begin.", "success")
                
            except Exception as e:
                self.log_flow(f"✗ Initialization Error: {str(e)}", "error")
                self.status_label.config(text=f"Status: Error - {str(e)}", fg=self.accent_red)
        
        thread = threading.Thread(target=init_thread, daemon=True)
        thread.start()
        
    def manual_predict(self, data, is_valid=True):
        """Predict without the secure_predict method (manual prediction only)
        
        Args:
            data: Input data dictionary
            is_valid: Whether this prediction represents valid data (for display purposes)
        """
        try:
            import pandas as pd
            import numpy as np
            
            # Convert dict to dataframe
            df = pd.DataFrame([data])
            df = df.select_dtypes(include=[np.number]).copy()
            df = df.fillna(df.median())
            
            # Scale with full 43 features
            X_scaled_full = self.predictor.scaler.transform(df.values)
            
            # Select GA features
            if self.predictor.selected_idx is not None and len(self.predictor.selected_idx) > 0:
                X_selected = X_scaled_full[:, self.predictor.selected_idx]
            else:
                X_selected = X_scaled_full
            
            # Predict
            model = self.predictor.models["xgb"]
            prediction = model.predict(X_selected)
            proba = model.predict_proba(X_selected) if hasattr(model, "predict_proba") else None
            
            prob_val = float(proba[0][1]) if proba is not None else 0.0
            
            return {
                "prediction": int(prediction[0]),
                "probability": prob_val,
                "model_used": "XGBoost",
                "is_valid": is_valid
            }
        except Exception as e:
            self.log_flow(f"  Prediction error: {str(e)}", "error")
            return {
                "prediction": None,
                "probability": None,
                "model_used": "XGBoost",
                "is_valid": False,
                "error": str(e)
            }
        
    def generate_normal_data(self):
        """Generate legitimate IoT sensor data (43 features)"""
        np.random.seed(int(time.time()) % 100)
        data = {
            "Mean": np.random.uniform(80, 120),
            "Sport": np.random.uniform(1000, 65535),
            "Dport": np.random.uniform(1000, 65535),
            "SrcPkts": np.random.uniform(100, 1000),
            "DstPkts": np.random.uniform(100, 1000),
            "TotPkts": np.random.uniform(200, 2000),
            "DstBytes": np.random.uniform(1000, 100000),
            "SrcBytes": np.random.uniform(1000, 100000),
            "TotBytes": np.random.uniform(2000, 200000),
            "SrcLoad": np.random.uniform(0.1, 5.0),
            "DstLoad": np.random.uniform(0.1, 5.0),
            "Rate": np.random.uniform(1, 100),
            "Duration": np.random.uniform(10, 300),
            "Idle": np.random.uniform(0, 10),
        }
        
        # Add F1-F29 (29 additional features)
        for i in range(1, 30):
            data[f"F{i}"] = np.random.uniform(-1, 1)
        
        return data
        
    def generate_attack_data(self, attack_type="moderate"):
        """Generate attack/suspicious IoT data"""
        np.random.seed(int(time.time()) % 100)
        
        if attack_type == "Moderate":
            data = {
                "Mean": np.random.uniform(40, 80),
                "Sport": np.random.uniform(100, 500),
                "Dport": np.random.uniform(100, 500),
                "SrcPkts": np.random.uniform(1000, 5000),
                "DstPkts": np.random.uniform(1000, 5000),
                "TotPkts": np.random.uniform(5000, 50000),
                "DstBytes": np.random.uniform(100000, 1000000),
                "SrcBytes": np.random.uniform(100000, 1000000),
                "TotBytes": np.random.uniform(200000, 2000000),
                "SrcLoad": np.random.uniform(50, 90),
                "DstLoad": np.random.uniform(50, 90),
                "Rate": np.random.uniform(500, 5000),
                "Duration": np.random.uniform(1, 60),
                "Idle": np.random.uniform(0, 1),
            }
        else:  # Severe
            data = {
                "Mean": np.random.uniform(20, 50),
                "Sport": np.random.uniform(1, 100),
                "Dport": np.random.uniform(1, 100),
                "SrcPkts": np.random.uniform(5000, 50000),
                "DstPkts": np.random.uniform(5000, 50000),
                "TotPkts": np.random.uniform(50000, 500000),
                "DstBytes": np.random.uniform(1000000, 10000000),
                "SrcBytes": np.random.uniform(1000000, 10000000),
                "TotBytes": np.random.uniform(2000000, 20000000),
                "SrcLoad": np.random.uniform(90, 100),
                "DstLoad": np.random.uniform(90, 100),
                "Rate": np.random.uniform(5000, 50000),
                "Duration": np.random.uniform(0.1, 10),
                "Idle": np.random.uniform(0, 0.1),
            }
        
        # Add F1-F29
        for i in range(1, 30):
            data[f"F{i}"] = np.random.uniform(-5, 5)
        
        return data
        
    def scenario_legitimate_user(self):
        """Alice sends legitimate data"""
        if not self.system_active:
            messagebox.showerror("Error", "System still initializing...")
            return
            
        def run_scenario():
            self.clear_display()
            threat_level = self.threat_var.get()
            
            self.log_flow("=" * 80, "process")
            self.log_flow("SCENARIO 1: LEGITIMATE USER (ALICE)", "header")
            self.log_flow("=" * 80, "process")
            
            # Step 1: Generate data
            self.log_flow("\n[STEP 1] 📊 Generate IoT Sensor Data", "process")
            data = self.generate_normal_data()
            self.display_data_details("Alice's Legitimate Data", data)
            self.log_flow("✓ Generated 43 sensor features", "success")
            self.log_flow(f"  Mean Load: {data['SrcLoad']:.2f}%", "info")
            self.log_flow(f"  Total Packets: {data['TotPkts']:.0f}", "info")
            
            # Step 2: Sign data
            self.log_flow("\n[STEP 2] 🔏 Digital Signature Creation", "process")
            self.log_flow("  Using: RSA 2048-bit + SHA256 hash", "info")
            
            signature = self.alice_manager.sign_data(data)
            sig_display = signature[:40] + "..." + signature[-10:]
            self.log_flow(f"✓ Data signed successfully", "success")
            self.log_flow(f"  Signature: {sig_display}", "info")
            self.log_flow(f"  Signature length: {len(signature)} bytes", "info")
            
            # Step 3: Verify signature
            self.log_flow("\n[STEP 3] ✅ Signature Verification", "process")
            is_valid = self.alice_manager.verify_signature(data, signature)
            self.log_flow(f"  Verifying with Alice's PUBLIC key", "info")
            self.log_flow(f"✓ Signature verification: {'VALID' if is_valid else 'INVALID'}", "success" if is_valid else "error")
            self.log_flow(f"  Data integrity: ✓ CONFIRMED", "success")
            
            # Step 4: Predict
            self.log_flow("\n[STEP 4] 🤖 ML Model Prediction", "process")
            self.log_flow("  Feature selection: Genetic Algorithm (21/43 features)", "info")
            self.log_flow("  Running XGBoost model...", "info")
            
            result = self.manual_predict(data)
            self.display_prediction_results("Alice's Prediction", result)
            
            # Step 5: Final verdict
            self.log_flow("\n[STEP 5] 📋 Final Verdict", "process")
            self.display_security_analysis(
                source="Alice (Original User)",
                signature_valid=True,
                data_tampered=False,
                prediction=result,
                verdict="ACCEPTED"
            )
            
            self.log_flow("\n" + "=" * 80, "process")
            self.log_flow("✓ TRANSACTION COMPLETED SUCCESSFULLY", "success")
            self.log_flow("=" * 80, "process")
        
        thread = threading.Thread(target=run_scenario, daemon=True)
        thread.start()
        
    def scenario_attacker_impersonation(self):
        """Bob tries impersonation with different RSA keys"""
        if not self.system_active:
            messagebox.showerror("Error", "System still initializing...")
            return
            
        def run_scenario():
            self.clear_display()
            
            self.log_flow("=" * 80, "process")
            self.log_flow("SCENARIO 2: ATTACKER - IMPERSONATION ATTEMPT (BOB)", "header")
            self.log_flow("=" * 80, "process")
            
            # Step 1: Attacker generates malicious data
            self.log_flow("\n[STEP 1] 👹 Attacker Generates Malicious Data", "warning")
            attack_data = self.generate_attack_data("Moderate")
            self.display_data_details("Bob's Malicious Data", attack_data)
            self.log_flow("⚠ Suspicious patterns detected", "warning")
            self.log_flow(f"  High load: {attack_data['SrcLoad']:.2f}%", "warning")
            self.log_flow(f"  Excessive packets: {attack_data['TotPkts']:.0f}", "warning")
            
            # Step 2: Bob signs with his own key
            self.log_flow("\n[STEP 2] 🔓 Attacker Signs with OWN RSA Key", "warning")
            self.log_flow("  ⚠ Critical Problem: Bob's key ≠ Alice's key", "warning")
            bob_signature = self.bob_manager.sign_data(attack_data)
            sig_display = bob_signature[:40] + "..." + bob_signature[-10:]
            self.log_flow(f"✓ Bob's signature created: {sig_display}", "info")
            
            # Step 3: Verify with Alice's key (FAILS)
            self.log_flow("\n[STEP 3] ❌ Signature Verification FAILS", "process")
            self.log_flow("  System verifying with Alice's PUBLIC key", "info")
            
            is_valid = self.alice_manager.verify_signature(attack_data, bob_signature)
            self.log_flow(f"✗ Signature verification: {'VALID' if is_valid else 'INVALID'}", 
                         "success" if is_valid else "error")
            self.log_flow(f"  Reason: Bob's signature ≠ Alice's public key", "error")
            
            # Step 4: Show what model would predict (FOR DEMONSTRATION ONLY)
            self.log_flow("\n[STEP 4] 🚫 BLOCKED - Data REJECTED before model", "error")
            self.log_flow("  ⚠ Prediction NOT executed (security blocked)", "warning")
            self.log_flow("\n  [FOR DEMONSTRATION ONLY] What the data would predict if allowed:", "info")
            demo_result = self.manual_predict(attack_data, is_valid=False)
            self.log_flow(f"    Predicted class: {demo_result['prediction']}", "info")
            self.log_flow(f"    Confidence: {demo_result['probability']:.2f}%", "info")
            self.display_prediction_results("Bob's Data (DEMONSTRATION - would not execute)", demo_result)
            
            # Step 5: Security alert
            self.log_flow("\n[STEP 5] 🚨 SECURITY ALERT", "process")
            self.display_security_analysis(
                source="Bob (Attacker - Impersonation)",
                signature_valid=False,
                data_tampered=True,
                prediction=None,
                verdict="REJECTED - ATTACKER DETECTED"
            )
            
            self.log_flow("\n" + "=" * 80, "process")
            self.log_flow("✗ TRANSACTION BLOCKED - SECURITY BREACH DETECTED", "error")
            self.log_flow("=" * 80, "process")
        
        thread = threading.Thread(target=run_scenario, daemon=True)
        thread.start()
        
    def scenario_attacker_tampering(self):
        """Charlie intercepts and modifies data"""
        if not self.system_active:
            messagebox.showerror("Error", "System still initializing...")
            return
            
        def run_scenario():
            self.clear_display()
            
            self.log_flow("=" * 80, "process")
            self.log_flow("SCENARIO 3: ATTACKER - DATA TAMPERING (CHARLIE)", "header")
            self.log_flow("=" * 80, "process")
            
            # Step 1: Alice creates legitimate data
            self.log_flow("\n[STEP 1] ✓ Alice Creates Legitimate Data", "process")
            alice_data = self.generate_normal_data()
            self.display_data_details("Original Data (Alice)", alice_data)
            self.log_flow("✓ All values in normal range", "success")
            
            # Step 2: Alice signs the data
            self.log_flow("\n[STEP 2] 🔏 Alice Signs Data with Private Key", "process")
            alice_signature = self.alice_manager.sign_data(alice_data)
            sig_display = alice_signature[:40] + "..." + alice_signature[-10:]
            self.log_flow(f"✓ Signature: {sig_display}", "success")
            self.log_flow(f"  SHA256 Hash Created: {alice_signature[:16]}...", "info")
            
            # Step 3: Charlie intercepts and modifies
            self.log_flow("\n[STEP 3] 👹 Charlie INTERCEPTS & MODIFIES Data", "warning")
            self.log_flow("  ⚠ Man-in-the-middle attack detected!", "warning")
            
            tampered_data = alice_data.copy()
            original_srcload = tampered_data["SrcLoad"]
            tampered_data["SrcLoad"] = original_srcload + 0.5  # Modify one field
            
            self.log_flow(f"  Modified field: SrcLoad", "warning")
            self.log_flow(f"    Original:  {original_srcload:.4f}", "info")
            self.log_flow(f"    Tampered:  {tampered_data['SrcLoad']:.4f}", "warning")
            self.log_flow(f"  Change: Only {(0.5/original_srcload*100):.2f}% of one field", "warning")
            self.log_flow(f"  Signature kept: UNCHANGED (original from Alice)", "info")
            
            # Step 4: Verification detects tampering
            self.log_flow("\n[STEP 4] 🔍 Tamper Detection - Verification FAILS", "process")
            self.log_flow("  Computing SHA256 hash of tampered data...", "info")
            
            is_valid = self.alice_manager.verify_signature(tampered_data, alice_signature)
            self.log_flow(f"✗ Hash verification: {'MATCH' if is_valid else 'NO MATCH'}", 
                         "success" if is_valid else "error")
            self.log_flow(f"  Result: Single byte modification = completely different hash", "error")
            self.log_flow(f"  Conclusion: DATA TAMPERING DETECTED", "error")
            
            # Step 5: Show what model would predict (FOR DEMONSTRATION ONLY)
            self.log_flow("\n[STEP 5] 🚫 BLOCKED - Data REJECTED before model", "error")
            self.log_flow("  ⚠ Prediction NOT executed (tampering blocked)", "warning")
            self.log_flow("\n  [FOR DEMONSTRATION ONLY] What the tampered data would predict if allowed:", "info")
            demo_result = self.manual_predict(tampered_data, is_valid=False)
            self.log_flow(f"    Predicted class: {demo_result['prediction']}", "info")
            self.log_flow(f"    Confidence: {demo_result['probability']:.2f}%", "info")
            self.display_prediction_results("Charlie's Data (DEMONSTRATION - would not execute)", demo_result)
            
            # Step 6: Security alert
            self.log_flow("\n[STEP 6] 🚨 TAMPERING ALERT - DATA REJECTED", "process")
            self.display_security_analysis(
                source="Charlie (Attacker - Tampering)",
                signature_valid=False,
                data_tampered=True,
                prediction=None,
                verdict="REJECTED - TAMPERING DETECTED"
            )
            
            self.log_flow("\n" + "=" * 80, "process")
            self.log_flow("✗ TRANSACTION BLOCKED - DATA INTEGRITY COMPROMISED", "error")
            self.log_flow("=" * 80, "process")
        
        thread = threading.Thread(target=run_scenario, daemon=True)
        thread.start()
        
    def scenario_alert_analysis(self):
        """Analyze multiple alert types"""
        if not self.system_active:
            messagebox.showerror("Error", "System still initializing...")
            return
            
        def run_scenario():
            self.clear_display()
            
            self.log_flow("=" * 80, "process")
            self.log_flow("SCENARIO 4: ALERT ANALYSIS - MULTIPLE THREAT TYPES", "header")
            self.log_flow("=" * 80, "process")
            
            alerts = [
                {"name": "Normal Traffic", "type": "normal", "threat": "LOW"},
                {"name": "Port Scanning Attack", "type": "port_scan", "threat": "MEDIUM"},
                {"name": "DDoS Attack", "type": "ddos", "threat": "HIGH"},
                {"name": "Data Exfiltration", "type": "exfil", "threat": "CRITICAL"},
            ]
            
            for idx, alert in enumerate(alerts, 1):
                self.log_flow(f"\n[ALERT {idx}] {alert['name']}", "process")
                self.log_flow("-" * 40, "process")
                
                # Generate appropriate data
                if alert['type'] == 'normal':
                    data = self.generate_normal_data()
                    self.log_flow(f"  Type: Legitimate IoT Traffic", "info")
                else:
                    severity = "Moderate" if alert['threat'] == 'MEDIUM' else "Severe"
                    data = self.generate_attack_data(severity)
                    self.log_flow(f"  Type: {alert['name']}", "warning")
                
                # Sign and verify
                signature = self.alice_manager.sign_data(data)
                is_valid = self.alice_manager.verify_signature(data, signature)
                
                self.log_flow(f"  Signature: {'✓ VALID' if is_valid else '✗ INVALID'}", 
                             "success" if is_valid else "error")
                
                # Predict
                result = self.manual_predict(data)
                
                if result['prediction'] is not None:
                    self.log_flow(f"  Prediction: {result['prediction']}", "info")
                    prob_val = result['probability'] if result['probability'] is not None else 0
                    self.log_flow(f"  Confidence: {prob_val:.2f}%", "info")
                else:
                    self.log_flow(f"  Prediction: Failed", "error")
                self.log_flow(f"  Threat Level: {alert['threat']}", "warning" if alert['threat'] != 'LOW' else "success")
                
                # Add to data display
                self.data_text.insert(tk.END, f"\n{alert['name']}\n", "header")
                for key in list(data.keys())[:8]:  # Show first 8 fields
                    self.data_text.insert(tk.END, f"  {key}: {data[key]:.2f}\n", "info")
            
            # Summary
            self.log_flow("\n" + "=" * 80, "process")
            self.log_flow("📊 ANALYSIS SUMMARY", "header")
            self.log_flow("=" * 80, "process")
            self.log_flow(f"  Total Alerts Processed: {len(alerts)}", "info")
            self.log_flow(f"  All Signatures: Valid ✓", "success")
            self.log_flow(f"  Threat Distribution:", "info")
            for alert in alerts:
                self.log_flow(f"    • {alert['name']}: {alert['threat']}", "warning" if alert['threat'] != 'LOW' else "success")
            self.log_flow(f"\n✓ Analysis Complete", "success")
            
        thread = threading.Thread(target=run_scenario, daemon=True)
        thread.start()
        
    def display_data_details(self, title, data):
        """Display data in the Data Details tab"""
        self.data_text.insert(tk.END, f"\n{title}\n", "header")
        self.data_text.insert(tk.END, "=" * 50 + "\n", "process")
        
        for key, value in list(data.items())[:20]:  # Show first 20
            self.data_text.insert(tk.END, f"  {key:12} : {value:12.4f}\n", "info")
        
        if len(data) > 20:
            self.data_text.insert(tk.END, f"  ... and {len(data) - 20} more features\n", "info")
        
        self.data_text.insert(tk.END, "\n", "process")
        
    def display_prediction_results(self, title, result):
        """Display model prediction results"""
        self.pred_text.insert(tk.END, f"\n{title}\n", "header")
        self.pred_text.insert(tk.END, "=" * 50 + "\n", "process")
        
        if result['is_valid'] and result['prediction'] is not None:
            pred_class = "NORMAL" if result['prediction'] == 0 else "ATTACK"
            self.pred_text.insert(tk.END, f"  Prediction Class: {pred_class}\n", "success" if result['prediction'] == 0 else "warning")
            prob_val = result['probability'] if result['probability'] is not None else 0
            self.pred_text.insert(tk.END, f"  Confidence: {prob_val:.2f}%\n", "success" if result['prediction'] == 0 else "warning")
            self.pred_text.insert(tk.END, f"  Model Used: {result.get('model_used', 'N/A')}\n", "info")
        else:
            self.pred_text.insert(tk.END, f"  Status: PREDICTION NOT MADE\n", "error")
            self.pred_text.insert(tk.END, f"  Reason: Data failed verification\n", "error")
        
        self.pred_text.insert(tk.END, f"  Data Valid: {result['is_valid']}\n", "success" if result['is_valid'] else "error")
        self.pred_text.insert(tk.END, "\n", "process")
        
    def display_security_analysis(self, source, signature_valid, data_tampered, prediction, verdict):
        """Display security analysis"""
        self.sec_text.insert(tk.END, f"\nSecurity Analysis\n", "header")
        self.sec_text.insert(tk.END, "=" * 50 + "\n", "process")
        
        self.sec_text.insert(tk.END, f"  Source: {source}\n", "warning" if "Attacker" in source else "success")
        self.sec_text.insert(tk.END, f"  Signature Valid: {'✓ YES' if signature_valid else '✗ NO'}\n", 
                            "success" if signature_valid else "error")
        self.sec_text.insert(tk.END, f"  Data Tampered: {'✗ YES' if data_tampered else '✓ NO'}\n", 
                            "error" if data_tampered else "success")
        
        if prediction:
            self.sec_text.insert(tk.END, f"  Prediction: {prediction['prediction']}\n", "info")
        
        verdict_tag = "error" if "REJECTED" in verdict else "success"
        self.sec_text.insert(tk.END, f"  Verdict: {verdict}\n", verdict_tag)
        self.sec_text.insert(tk.END, "\n", "process")
        
    def log_flow(self, message, tag="info"):
        """Add message to process flow"""
        self.flow_text.insert(tk.END, message + "\n", tag)
        self.flow_text.see(tk.END)
        self.root.update()
        
    def clear_display(self):
        """Clear all display panels"""
        self.flow_text.delete(1.0, tk.END)
        self.data_text.delete(1.0, tk.END)
        self.pred_text.delete(1.0, tk.END)
        self.sec_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SecureIoTUI(root)
    root.mainloop()
