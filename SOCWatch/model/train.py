import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

def train_model(input_path="../data/combined_dataset.csv", model_path="output/threat_detector.pkl"):
    # Load dataset
    df = pd.read_csv(input_path)

    # Clean invalid values
    df.replace([float('inf'), float('-inf')], 0, inplace=True)
    df.fillna(0, inplace=True)

    # Split features & label
    X = df.drop("label", axis=1)
    y = df["label"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Save model
    import os
    os.makedirs("model", exist_ok=True)
    joblib.dump(clf, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
