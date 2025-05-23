import pandas as pd
import os
import random
from datetime import datetime

def extract_misp_like_cicids(input_path="../data/suspicious_logs.csv", output_path="../data/suspicious_features.csv"):
    df = pd.read_csv(input_path)

    # Basic timestamp to hour
    df['hour'] = pd.to_datetime(df['timestamp'], errors='coerce').dt.hour.fillna(-1).astype(int)

    # Simulate flow-like values (random or fixed mapping)
    df["Destination Port"] = df["ioc_type"].apply(lambda x: 80 if "domain" in x else 443 if "link" in x else 53)
    df["Flow Duration"] = random.choices(range(1, 1000), k=len(df))
    df["Total Fwd Packets"] = random.choices(range(1, 10), k=len(df))
    df["Total Backward Packets"] = random.choices(range(0, 5), k=len(df))
    df["Packet Length Mean"] = random.choices(range(20, 1500), k=len(df))
    df["Fwd Packet Length Mean"] = random.choices(range(20, 800), k=len(df))
    df["Bwd Packet Length Mean"] = random.choices(range(0, 600), k=len(df))
    df["Fwd PSH Flags"] = random.choices([0, 1], k=len(df))
    df["SYN Flag Count"] = random.choices([0, 1], k=len(df))
    df["ACK Flag Count"] = 1  # we assume ACK always exists
    df["Flow Bytes/s"] = random.choices(range(100000, 10000000), k=len(df))

    # Final clean structure
    features = [
        "Destination Port", "Flow Duration", "Total Fwd Packets", "Total Backward Packets",
        "Packet Length Mean", "Fwd Packet Length Mean", "Bwd Packet Length Mean",
        "Fwd PSH Flags", "SYN Flag Count", "ACK Flag Count", "Flow Bytes/s", "label"
    ]

    df["label"] = 1  # All are suspicious
    df = df[features]

    os.makedirs("data", exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Simulated suspicious flow-like features saved to {output_path}")

if __name__ == "__main__":
    extract_misp_like_cicids()
