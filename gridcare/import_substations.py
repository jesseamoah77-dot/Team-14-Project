import os
import sqlite3
import pandas as pd

#  set file paths relative to this script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'Substations.csv')
DB_PATH = os.path.join(BASE_DIR, 'gridcare.db')


def import_substations(csv_path=CSV_PATH, db_path=DB_PATH):
    # 1. Locate the CSV file (checks gridcare directory first, then root)
    if not os.path.exists(csv_path):
        root_csv = os.path.join(os.path.dirname(BASE_DIR), 'Substations.csv')
        if os.path.exists(root_csv):
            csv_path = root_csv
        else:
            print(f"Error: Could not find '{csv_path}' or '{root_csv}'.")
            return

    # 2. Read and clean the CSV data
    print(f"Reading substations from: {csv_path}")
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()  # Remove trailing whitespace in headers

    # Rename CSV columns to match database field names
    df = df.rename(columns={
        'Substation ID': 'substation_id',
        'Name': 'name',
        'Region': 'region'
    })

    # Validate required columns exist
    required_cols = ['substation_id', 'name', 'region']
    if not all(col in df.columns for col in required_cols):
        print(f"Error: CSV is missing one of required columns: {required_cols}")
        return

    subset = df[required_cols].dropna(subset=['substation_id'])

    # 3. Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Ensure the substations table exists
    cur.execute('''
        CREATE TABLE IF NOT EXISTS substations (
            substation_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            region TEXT NOT NULL
        )
    ''')

    # 4. Insert data into database
    rows_inserted = 0
    for _, row in subset.iterrows():
        cur.execute(
            '''
            INSERT OR IGNORE INTO substations (substation_id, name, region)
            VALUES (?, ?, ?)
            ''',
            (int(row['substation_id']), str(row['name']), str(row['region']))
        )
        rows_inserted += cur.rowcount

    conn.commit()

    # 5. Output summary results
    cur.execute('SELECT COUNT(*) FROM substations')
    total = cur.fetchone()[0]
    print(f"Newly inserted rows this run: {rows_inserted}")
    print(f"Total substations now in database: {total}")

    conn.close()


if __name__ == '__main__':
    import_substations()
