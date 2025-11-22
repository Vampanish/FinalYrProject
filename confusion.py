import os
import pandas as pd
import matplotlib.pyplot as plt

# 🔹 Base directory where model folders are stored
BASE_DIR = "E:/Final Yr Project/code"  # change if needed

# 🔹 Model folders from 100k to 1M
folders = [f"models_sample{i}k" for i in range(100, 1100, 100)]  # 100k–1000k
sizes = [i for i in range(100, 1100, 100)]

# Stop at 1M
folders = folders[:10]
sizes = sizes[:10]

# 🔹 Initialize training time storage
train_times = {"KNN": [], "DT": [], "XGBoost": [], "NaiveBayes": []}

for folder in folders:
    csv_path = os.path.join(BASE_DIR, folder, "model_comparison.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, index_col=0)
        train_times["KNN"].append(df.loc["KNN", "TrainTime_s"])
        train_times["DT"].append(df.loc["DT", "TrainTime_s"])
        train_times["XGBoost"].append(df.loc["XGBoost", "TrainTime_s"])
        train_times["NaiveBayes"].append(df.loc["NaiveBayes", "TrainTime_s"])
    else:
        print(f"⚠ Missing: {csv_path}")
        for key in train_times:
            train_times[key].append(None)

# 🔹 X-axis labels in k format (e.g., 200k, 400k, 600k, 800k, 1M)
labels = [f"{s}k" if s != 1000 else "1M" for s in sizes]

# 🔹 Plotting
plt.figure(figsize=(9, 5))
plt.plot(sizes, train_times["KNN"], marker='o', label="KNN", linewidth=2)
plt.plot(sizes, train_times["DT"], marker='s', label="Decision Tree", linewidth=2)
plt.plot(sizes, train_times["XGBoost"], marker='^', label="XGBoost", linewidth=2)
plt.plot(sizes, train_times["NaiveBayes"], marker='d', label="Naive Bayes", linewidth=2)

plt.xticks(sizes, labels)
plt.title("Training Time vs Dataset Size (All Models)", fontsize=13, pad=15)
plt.xlabel("Dataset Size", fontsize=12)
plt.ylabel("Training Time (seconds)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title="Model", loc='upper left', frameon=True)
plt.tight_layout()

plt.show()
# plt.savefig("training_time_vs_dataset_size_till_1M.png", dpi=300)
