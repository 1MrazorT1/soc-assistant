import pandas as pd
import joblib

def load_model(path="output/threat_detector.pkl"):
    return joblib.load(path)

def predict_csv(input_csv="../data/test_logs.csv"):
    model = load_model()
    df = pd.read_csv(input_csv)

    # Drop label column if present (used for evaluation, not prediction)
    if "label" in df.columns:
        y_true = df["label"]
        df = df.drop("label", axis=1)
    else:
        y_true = None

    predictions = model.predict(df)
    probabilities = model.predict_proba(df).max(axis=1)

    df["predicted"] = predictions
    df["confidence"] = probabilities

    if y_true is not None:
        df["true_label"] = y_true
        accuracy = (predictions == y_true).mean()
        print(f"Accuracy on test set: {accuracy:.4f}")

    print(df[["predicted", "confidence"]])
    return df

if __name__ == "__main__":
    predict_csv()
