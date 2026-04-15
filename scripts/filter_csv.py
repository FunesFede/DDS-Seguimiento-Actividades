import pandas as pd
import sys
from pathlib import Path


def filter_csv(file1_path: str, file2_path: str, output_path: str = None):
    """
    Filter rows in file2 where 'ID number' matches any value in file1.

    Args:
        file1_path: Source file — IDs to keep
        file2_path: File to filter by 'ID number' column
        output_path: Output path (default: filtered_<file2_name>)
    """
    file2_name = Path(file2_path).stem
    if output_path is None:
        output_path = f"filtered_{file2_name}.csv"

    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)

    column = "ID number"

    if column not in df2.columns:
        raise ValueError(f"Column '{column}' not found in {file2_path}. "
                         f"Available columns: {list(df2.columns)}")

    # Use first column of file1 as the ID source if it doesn't have 'ID number'
    if column in df1.columns:
        valid_ids = set(df1[column].dropna())
    else:
        valid_ids = set(df1.iloc[:, 0].dropna())

    filtered = df2[df2[column].isin(valid_ids)]

    filtered.to_csv(output_path, index=False)
    print(f"Done. {len(filtered)}/{len(df2)} rows kept → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python filter_csv.py <file1.csv> <file2.csv> [output.csv]")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None

    filter_csv(file1, file2, output)
