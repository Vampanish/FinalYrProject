import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# F1 values (ordered: XGBoost → KNN → Decision Tree → Naive Bayes)
data = {
    'Model': ['XGBoost', 'KNN', 'Decision Tree', 'Naive Bayes'],
    'F1 Score': [0.999657, 0.998713, 0.999399, 0.915716]
}

df = pd.DataFrame(data)

# Mild pastel colors
colors = ['#F7DC6F', '#AED6F1', '#A9DFBF', '#F5B7B1']  # yellow, blue, green, red

plt.figure(figsize=(7, 4))
sns.barplot(x='Model', y='F1 Score', data=df, palette=colors, edgecolor='gray')

# Add F1 values above bars with spacing
for i, val in enumerate(df['F1 Score']):
    plt.text(i, val + 0.002, f'{val:.6f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Title and labels with padding
plt.title('F1 Comparison Across Models', fontsize=14, pad=20)
plt.xlabel('Models', fontsize=12, labelpad=10)
plt.ylabel('F1 Score', fontsize=12, labelpad=10)

# Adjust y-axis for visibility of differences
plt.ylim(0.90, 1.001)

# Add soft gridlines
plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()
