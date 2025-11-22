import matplotlib.pyplot as plt
import pandas as pd

# Dataset sizes
sizes = [100_000, 200_000, 300_000, 400_000, 500_000, 600_000, 700_000, 800_000, 900_000, 1_000_000, 1_100_000]
labels = [f"{s//1000}k" for s in sizes]  # converts 100000 -> 100k

# Replace with your real times
time_knn = [0.12, 0.15, 0.17, 0.19, 0.22, 0.25, 0.28, 0.3, 0.33, 0.36, 0.39]
time_dt = [0.3, 0.45, 0.6, 0.8, 1.0, 1.2, 1.35, 1.5, 1.7, 1.9, 2.1]
time_xgb = [0.4, 0.6, 0.8, 1.0, 1.25, 1.45, 1.7, 1.9, 2.2, 2.5, 2.8]
time_nb = [0.1, 0.12, 0.13, 0.15, 0.16, 0.18, 0.19, 0.2, 0.22, 0.23, 0.25]

plt.figure(figsize=(9,5))
plt.plot(sizes, time_knn, marker='o', label='KNN', linewidth=2)
plt.plot(sizes, time_dt, marker='s', label='Decision Tree', linewidth=2)
plt.plot(sizes, time_xgb, marker='^', label='XGBoost', linewidth=2)
plt.plot(sizes, time_nb, marker='d', label='Naive Bayes', linewidth=2)

plt.xticks(sizes, labels)  # ✅ shows 100k, 200k, etc
plt.title("Training Time vs Dataset Size (All Models)", fontsize=13, pad=15)
plt.xlabel("Dataset Size", fontsize=12)
plt.ylabel("Training Time (seconds)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title="Model", loc='upper left', frameon=True)
plt.tight_layout()

plt.show()
# plt.savefig("training_time_vs_dataset_size.png", dpi=300)
