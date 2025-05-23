import pandas as pd

def merge_datasets(benign_path, suspicious_path, output_path):
    # Load both datasets
    benign_df = pd.read_csv(benign_path)
    suspicious_df = pd.read_csv(suspicious_path)

    # Ensure same columns and structure
    if list(benign_df.columns) != list(suspicious_df.columns):
        raise ValueError("Columns do not match between benign and suspicious datasets.")

    # Concatenate and shuffle
    combined_df = pd.concat([benign_df, suspicious_df], ignore_index=True)
    combined_df = combined_df.sample(frac=1).reset_index(drop=True)

    # Save
    combined_df.to_csv(output_path, index=False)
    print(f"Merged dataset saved to {output_path} with {len(combined_df)} rows")

# Example usage
if __name__ == "__main__":
    merge_datasets(
        benign_path="../data/benign_features.csv",
        suspicious_path="../data/suspicious_features.csv",
        output_path="../data/combined_dataset.csv"
    )
