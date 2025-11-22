import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
import warnings, time, os

warnings.filterwarnings("ignore")

CSV_FILE = "wustl_iiot_2021.csv"
SAMPLE_SIZE = 300_000
TEST_SIZE = 0.3
RANDOM_STATE = 42

QGA_POP = 12
QGA_GENS = 8
QGA_NQUBITS = 40
KNN_NEIGH = 5
DT_MAX_DEPTH = 12

OUT_DIR = "models_sample300k"
os.makedirs(OUT_DIR, exist_ok=True)

print("1) Loading dataset and drawing stratified sample...")
df = pd.read_csv(CSV_FILE)
if "Target" not in df.columns:
    raise RuntimeError("Target column 'Target' not found in CSV.")

df = df.dropna(subset=["Target"])
if len(df) <= SAMPLE_SIZE:
    sample_df = df
    print(f"Dataset has {len(df)} rows; using full dataset.")
else:
    sample_df = df.groupby("Target", group_keys=False).apply(
        lambda x: x.sample(frac=min(1, SAMPLE_SIZE/len(df)), random_state=RANDOM_STATE)
    )
    if len(sample_df) > SAMPLE_SIZE:
        sample_df = sample_df.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE)

print("Sample shape:", sample_df.shape)
print("Class counts:\n", sample_df["Target"].value_counts())

print("\n2) Preprocessing (numeric-only, scaling)...")
y = sample_df["Target"].astype(int)
X = sample_df.drop(columns=["Target"]).select_dtypes(include=[np.number]).copy()
X = X.fillna(X.median())

orig_columns = list(X.columns)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)
print("Train/test shapes:", X_train.shape, X_test.shape)

print("\n3) Running lightweight QGA for feature selection...")
rng = np.random.default_rng(RANDOM_STATE)
n_features = X_train.shape[1]
n_qubits = min(QGA_NQUBITS, n_features)

def init_population(pop_size, n_q):
    return rng.random((pop_size, n_q)) * 0.98 + 0.01

def measure_state(probs):
    return (rng.random(probs.shape) < probs).astype(int)

def fitness_binary(chrom):
    idx = np.where(chrom == 1)[0]
    if len(idx) == 0:
        return 0.0
    clf = XGBClassifier(n_estimators=50, max_depth=5, learning_rate=0.1,
                        subsample=0.8, use_label_encoder=False, eval_metric="logloss",
                        random_state=RANDOM_STATE)
    try:
        scores = cross_val_score(clf, X_train[:, idx], y_train, cv=3, scoring="accuracy", n_jobs=1)
        return float(np.mean(scores))
    except Exception:
        return 0.0

population = init_population(QGA_POP, n_qubits)
best_state = None
best_score = 0.0

for gen in range(QGA_GENS):
    measured = measure_state(population)
    fitnesses = np.array([fitness_binary(ch) for ch in measured])
    gen_best_idx = int(np.argmax(fitnesses))
    gen_best_score = float(fitnesses[gen_best_idx])
    gen_best_state = measured[gen_best_idx]

    if gen_best_score > best_score:
        best_score = gen_best_score
        best_state = gen_best_state.copy()

    for i in range(QGA_POP):
        for j in range(n_qubits):
            if measured[i, j] != best_state[j]:
                population[i, j] += 0.06 if measured[i, j] < best_state[j] else -0.06
                population[i, j] = np.clip(population[i, j], 0.01, 0.99)

    print(f" Generation {gen+1}/{QGA_GENS} | Gen best acc: {gen_best_score:.4f} | Overall best: {best_score:.4f}")

if best_state is None:
    variances = np.var(X_train, axis=0)
    selected_idx = np.argsort(variances)[-30:]
else:
    selected_idx = np.where(best_state == 1)[0]
    if len(selected_idx) == 0:
        variances = np.var(X_train, axis=0)
        selected_idx = np.argsort(variances)[-30:]
    elif len(selected_idx) > 100:
        variances = np.var(X_train[:, selected_idx], axis=0)
        order = np.argsort(variances)[-50:]
        selected_idx = selected_idx[order]

selected_cols = [orig_columns[i] for i in selected_idx]
print("Selected features:", selected_cols)
joblib.dump(selected_idx, os.path.join(OUT_DIR, "selected_idx.npy"))
joblib.dump(selected_cols, os.path.join(OUT_DIR, "selected_cols.pkl"))
joblib.dump(scaler, os.path.join(OUT_DIR, "scaler.pkl"))

X_train_sel = X_train[:, selected_idx]
X_test_sel = X_test[:, selected_idx]

results = {}

print("\n4.1) Training KNN...")
knn = KNeighborsClassifier(n_neighbors=KNN_NEIGH, n_jobs=-1)
t0 = time.time()
knn.fit(X_train_sel, y_train)
t1 = time.time()
y_pred = knn.predict(X_test_sel)
results["KNN"] = {
    "Accuracy": accuracy_score(y_test, y_pred),
    "Precision": precision_score(y_test, y_pred, zero_division=0),
    "Recall": recall_score(y_test, y_pred, zero_division=0),
    "F1": f1_score(y_test, y_pred, zero_division=0),
    "ROC-AUC": roc_auc_score(y_test, knn.predict_proba(X_test_sel)[:, 1]),
    "TrainTime_s": t1 - t0
}
joblib.dump(knn, os.path.join(OUT_DIR, "knn_model.pkl"))

print("\n4.2) Training Decision Tree...")
dt = DecisionTreeClassifier(max_depth=DT_MAX_DEPTH, random_state=RANDOM_STATE)
t0 = time.time()
dt.fit(X_train_sel, y_train)
t1 = time.time()
y_pred = dt.predict(X_test_sel)
results["DT"] = {
    "Accuracy": accuracy_score(y_test, y_pred),
    "Precision": precision_score(y_test, y_pred, zero_division=0),
    "Recall": recall_score(y_test, y_pred, zero_division=0),
    "F1": f1_score(y_test, y_pred, zero_division=0),
    "ROC-AUC": roc_auc_score(y_test, dt.predict_proba(X_test_sel)[:, 1]),
    "TrainTime_s": t1 - t0
}
joblib.dump(dt, os.path.join(OUT_DIR, "dt_model.pkl"))

print("\n4.3) Training XGBoost...")
xgb = XGBClassifier(n_estimators=150, max_depth=6, learning_rate=0.08,
                    subsample=0.9, colsample_bytree=0.9,
                    use_label_encoder=False, eval_metric="logloss",
                    random_state=RANDOM_STATE)
t0 = time.time()
xgb.fit(X_train_sel, y_train)
t1 = time.time()
y_pred = xgb.predict(X_test_sel)
results["XGBoost"] = {
    "Accuracy": accuracy_score(y_test, y_pred),
    "Precision": precision_score(y_test, y_pred, zero_division=0),
    "Recall": recall_score(y_test, y_pred, zero_division=0),
    "F1": f1_score(y_test, y_pred, zero_division=0),
    "ROC-AUC": roc_auc_score(y_test, xgb.predict_proba(X_test_sel)[:, 1]),
    "TrainTime_s": t1 - t0
}
joblib.dump(xgb, os.path.join(OUT_DIR, "xgb_model.pkl"))

print("\n4.4) Training Naive Bayes...")
nb = GaussianNB()
t0 = time.time()
nb.fit(X_train_sel, y_train)
t1 = time.time()
y_pred = nb.predict(X_test_sel)
results["NaiveBayes"] = {
    "Accuracy": accuracy_score(y_test, y_pred),
    "Precision": precision_score(y_test, y_pred, zero_division=0),
    "Recall": recall_score(y_test, y_pred, zero_division=0),
    "F1": f1_score(y_test, y_pred, zero_division=0),
    "ROC-AUC": roc_auc_score(y_test, nb.predict_proba(X_test_sel)[:, 1]),
    "TrainTime_s": t1 - t0
}
joblib.dump(nb, os.path.join(OUT_DIR, "naivebayes_model.pkl"))

print("\n5) Model Comparison Results:")
res_df = pd.DataFrame(results).T
print(res_df)
res_df.to_csv(os.path.join(OUT_DIR, "model_comparison.csv"), index=True)
print(f"\n✅ Results and models saved in '{OUT_DIR}'")
    "F1": f1_score(y_test, y_pred, zero_division=0),
