# cli.py
import argparse
import argparse
from feature_extraction import extract_features

def main():
    parser = argparse.ArgumentParser(description="Feature Extraction from Time Series Data")
    parser.add_argument("input_file", type=float, help="Path to the input file containing time series data.")
    args = parser.parse_args()

    # Assume the user has already loaded the Excel file into a DataFrame
    # Read the DataFrame directly from the input file path
    data = args.input_file
    first_column = data.iloc[:, 0]

    # Extract features
    df_with_features, correlated_pairs = extract_features(data,first_column)

    # Do something with the extracted features
    print("DataFrame with features:")
    print(df_with_features)
    print("Correlated pairs:")
    print(correlated_pairs)

if __name__ == "__main__":
    main()

