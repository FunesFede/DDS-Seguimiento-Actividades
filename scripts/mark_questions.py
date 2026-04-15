import pandas as pd
import sys
from pathlib import Path


def mark_source(source_path: str, filtered_path: str, output_path: str = None):
    """
    Adds a column to source_file named after the filtered file,
    marking 'Si' if the ID was found in the filtered file, 'No' otherwise.

    Args:
        source_path:   The original master file (file1)
        filtered_path: The filtered CSV produced by filter_csv.py
        output_path:   Where to save the result (default: overwrites source)
    """
    if output_path is None:
        output_path = source_path

    column = "ID number"
    new_col = Path(filtered_path).stem  # Column name = filtered file's name

    source_df = pd.read_csv(source_path)
    filtered_df = pd.read_csv(filtered_path)

    if column not in source_df.columns:
        raise ValueError(f"Column '{column}' not found in {source_path}. "
                         f"Available columns: {list(source_df.columns)}")

    if column not in filtered_df.columns:
        raise ValueError(f"Column '{column}' not found in {filtered_path}. "
                         f"Available columns: {list(filtered_df.columns)}")

    found_ids = set(filtered_df[column].dropna())
    source_df[new_col] = source_df[column].apply(
        lambda x: "Si" if x in found_ids else "No"
    )

    source_df.to_csv(output_path, index=False)

    matched = source_df[new_col].value_counts().get("Si", 0)
    print(
        f"Done. {matched}/{len(source_df)} marked 'Si' → column '{new_col}' added to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python mark_questions.py <source_file.csv> <questions_file.csv> [output.csv]")
        sys.exit(1)

    source = sys.argv[1]
    filtered = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None

    mark_source(source, filtered, output)
