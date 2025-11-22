from secure_predictor import SecureIoTPredictor

predictor = SecureIoTPredictor()
predictor.setup_keys(generate_new=False)

data = {f'F{i}': 0.5 for i in range(43)}

result = predictor.secure_predict(data, 'xgb')

print(f"Prediction: {result['prediction']}")
print(f"Valid: {result['is_valid']}")
print(f"Source: {result.get('source', 'N/A')}")
print(f"Error: {result.get('error', 'None')}")
