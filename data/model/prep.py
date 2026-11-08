import pandas as pd
from sklearn.model_selection import train_test_split

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
df = pd.read_csv(ROOT / "tourism_project/data/tourism.csv")
df.drop(columns=["CustomerID"], inplace=True)


target = "ProdTaken"
X = df.drop(columns=[target])
y = df[target]


Xtrain, Xtest, ytrain, ytest = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

Xtrain.to_csv(ROOT / "Xtrain.csv", index=False)
Xtest.to_csv(ROOT / "Xtest.csv", index=False)
ytrain.to_csv(ROOT / "ytrain.csv", index=False)
ytest.to_csv(ROOT / "ytest.csv", index=False)

print("Data prepared: train/test splits written.")
print("ProdTaken distribution in train:")
print(ytrain.value_counts())
