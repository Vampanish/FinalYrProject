import matplotlib.pyplot as plt
import numpy as np

# Data
models = ['KNN', 'Decision Tree', 'XGBoost', 'Naive Bayes']
train_time = [0.057293, 1.682402, 1.646527, 0.175545]
accuracy = [0.9998125, 0.9999125, 0.99995, 0.986613]
f1_score = [0.998713, 0.999399, 0.999657, 0.915716]

# Normalize accuracy and F1 to visualize better beside training time
acc_scaled = [a * 10 for a in accuracy]       # amplify metric values
f1_scaled = [f * 10 for f in f1_score]

plt.figure(figsize=(9,6))
plt.plot(models, train_time, marker='o', linewidth=3, color='#ef233c', label='Training Time (s)')
plt.plot(models, acc_scaled, marker='s', linewidth=3, color='#00b4d8', label='Accuracy ×10')
plt.plot(models, f1_scaled, marker='^', linewidth=3, color='#8338ec', label='F1-score ×10')

# Add annotations
for i, val in enumerate(train_time):
    plt.text(i, val + 0.05, f"{val:.3f}s", ha='center', fontsize=9, fontweight='bold', color='#ef233c')

for i, val in enumerate(accuracy):
    plt.text(i, val * 10 + 0.05, f"{val:.4f}", ha='center', fontsize=9, fontweight='bold', color='#00b4d8')

for i, val in enumerate(f1_score):
    plt.text(i, val * 10 - 0.25, f"{val:.4f}", ha='center', fontsize=9, fontweight='bold', color='#8338ec')

plt.title('Training Time vs Performance Metric Trade-off (400K Sample)', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Machine Learning Models', fontsize=12)
plt.ylabel('Scaled Value', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title="Metrics", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
# plt.savefig("training_time_tradeoff_linechart.png", dpi=300)
