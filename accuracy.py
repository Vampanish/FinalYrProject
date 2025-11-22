import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Accuracy values (in desired order)
data = {
    'Model': ['XGBoost', 'KNN', 'Decision Tree', 'Naive Bayes'],
    'Recall': [0.999485, 0.996827, 0.999142, 0.998284]
}

df = pd.DataFrame(data)

# Mild pastel colors
colors = ['#F7DC6F', '#AED6F1', '#A9DFBF', '#F5B7B1']  # soft gold, blue, green, red

plt.figure(figsize=(7, 4))
sns.barplot(x='Model', y='Recall', data=df, palette=colors, edgecolor='gray')

# Add accuracy values above bars with better spacing
for i, val in enumerate(df['Recall']):
    plt.text(i, val + 0.00001, f'{val:.6f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Title and labels
plt.title('Recall Comparison Across Models', fontsize=14, pad=20)  # pad adds space
plt.xlabel('Models', fontsize=12, labelpad=10)
plt.ylabel('Recall', fontsize=12, labelpad=10)

# Adjust y-limits for more vertical room
plt.ylim(0.9800, 1.003)

# Add mild gridlines
plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()
