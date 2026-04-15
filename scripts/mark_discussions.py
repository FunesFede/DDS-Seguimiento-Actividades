import pandas as pd
import sys


def mark_discussions_by_name(source_path: str, discussion_path: str, output_path: str = None):
    """
    For each unique 'subject' in discussion_path, adds a column to source_path.
    Matches students by full name (source: 'First name' + 'Last name' vs discussion: 'userfullname').
    Marks 'Si' if the student participated in that subject, 'No' otherwise.

    source_path:     Master file with student names (columns: 'First name', 'Last name')
    discussion_path: Discussion export with columns 'userfullname' and 'subject'
    output_path:     Where to save (default: overwrites source)
    """
    if output_path is None:
        output_path = source_path

    source_df = pd.read_csv(source_path)
    disc_df = pd.read_csv(discussion_path)

    # Build normalized full name in source
    source_df['_full_name'] = (
        source_df['First name'].str.strip() + ' ' + source_df['Last name'].str.strip()
    ).str.lower()

    disc_df['_full_name'] = disc_df['userfullname'].str.strip().str.lower()

    subjects = disc_df['subject'].unique()
    print(f"Found {len(subjects)} subject(s): {list(subjects)}\n")

    for subject in subjects:
        found_names = set(
            disc_df.loc[disc_df['subject'] == subject, '_full_name'].dropna()
        )
        action = "updated" if subject in source_df.columns else "created"
        source_df[subject] = source_df['_full_name'].apply(
            lambda x: "Si" if x in found_names else "No"
        )
        matched = (source_df[subject] == "Si").sum()
        print(f"  '{subject}' ({action}): {matched}/{len(source_df)} marked 'Si'")

    source_df.drop(columns=['_full_name'], inplace=True)
    source_df.to_csv(output_path, index=False)
    print(f"\nDone → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python mark_discussions.py <source.csv> <discussion.csv> [output.csv]")
        sys.exit(1)

    source = sys.argv[1]
    discussion = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) > 3 else None

    mark_discussions_by_name(source, discussion, output)
