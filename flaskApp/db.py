import sqlite3
import json

def get_db_structure(db_path, output_json_file):
    """
    Retrieves tables and columns from a SQLite database and saves them as a JSON file.

    Args:
        db_path (str): Path to the SQLite database file.
        output_json_file (str): Path to the output JSON file.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Dictionary to store the database structure
    db_structure = {}

    for table in tables:
        table_name = table[0]

        # Query to get column details for each table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        # Extract column details
        db_structure[table_name] = [
            {"column_name": column[1], "data_type": column[2], "not_null": bool(column[3]), "default_value": column[4]}
            for column in columns
        ]

    # Close the connection
    conn.close()

    # Save the structure as a JSON file
    with open(output_json_file, 'w') as json_file:
        json.dump(db_structure, json_file, indent=4)

    print(f"Database structure saved to {output_json_file}")

# Usage
db_path = "base.db"  # Path to your SQLite database file
output_json_file = "db_structure.json"  # Path to output JSON file
get_db_structure(db_path, output_json_file)
