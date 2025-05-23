import pandas as pd

def process_cicids_benign(input_path, output_path):
    # Load CSV
    df = pd.read_csv(input_path)

    # Strip column names to avoid issues with spaces like " Label"
    df.columns = df.columns.str.strip()

    # Filter only benign samples
    benign_df = df[df["Label"] == "BENIGN"].copy()

    # Replace problematic values
    benign_df.replace("Infinity", 0, inplace=True)
    benign_df.fillna(0, inplace=True)

    # Select relevant features for model training
    features = [
        "Destination Port", "Flow Duration", "Total Fwd Packets", "Total Backward Packets",
        "Packet Length Mean", "Fwd Packet Length Mean", "Bwd Packet Length Mean",
        "Fwd PSH Flags", "SYN Flag Count", "ACK Flag Count", "Flow Bytes/s"
    ]

    # Keep selected features and label them as benign (0)
    benign_df = benign_df[features]
    benign_df["label"] = 0

    # Save to output
    benign_df.to_csv(output_path, index=False)
    print(f"Saved {len(benign_df)} benign logs to {output_path}")

# Example usage
if __name__ == "__main__":
    process_cicids_benign(
        input_path="../data/Monday-WorkingHours.pcap_ISCX.csv",
        output_path="../data/benign_features.csv"
    )
