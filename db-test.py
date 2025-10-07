import sqlite3

# Define the database file name
DB_FILE = 'user_data.db'
TABLE_NAME = 'users'

# Data to insert
NEW_USER_NAME = 'Alice Smith'
NEW_USER_EMAIL = 'alice.smith@example.com'


def setup_database():
    """Opens the database, creates the table if necessary, and returns the connection and cursor."""
    try:
        # Connect to the SQLite database. It will be created if it doesn't exist.
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
        ''')
        conn.commit()
        print(f"✅ Database '{DB_FILE}' opened successfully.")
        print(f"✅ Table '{TABLE_NAME}' ensured/created successfully.")
        return conn, cursor

    except sqlite3.Error as e:
        print(f"❌ An error occurred during setup: {e}")
        return None, None

def insert_record(conn, cursor, name, email):
    """Inserts a new record into the users table."""
    try:
        # Use a parameterized query to safely insert data
        cursor.execute(f'''
            INSERT INTO {TABLE_NAME} (name, email)
            VALUES (?, ?);
        ''', (name, email))
        conn.commit()
        print(f"✅ Record inserted successfully for: {name}")

    except sqlite3.IntegrityError:
        # This handles the case where the email is already in the database (due to UNIQUE constraint)
        print(f"⚠️ Record NOT inserted. Email '{email}' already exists in the table.")
        
    except sqlite3.Error as e:
        print(f"❌ An error occurred during insertion: {e}")

def display_records(cursor):
    """Selects and displays all records from the users table."""
    try:
        # Select all records
        cursor.execute(f'SELECT id, name, email FROM {TABLE_NAME};')
        
        # Fetch all results
        records = cursor.fetchall()

        if not records:
            print(f"\nℹ️ The table '{TABLE_NAME}' is empty.")
            return

        print(f"\n📚 All Records in '{TABLE_NAME}':")
        # Print a simple header
        print("-" * 40)
        print(f"{'ID':<4} | {'Name':<15} | {'Email'}")
        print("-" * 40)

        # Iterate and display the records
        for row in records:
            # Unpack the tuple: (id, name, email)
            record_id, name, email = row
            print(f"{record_id:<4} | {name:<15} | {email}")
        print("-" * 40)

    except sqlite3.Error as e:
        print(f"❌ An error occurred during selection: {e}")


# --- Main Execution ---
if __name__ == '__main__':
    
    # 1. Open database and create table
    conn, cursor = setup_database()

    if conn and cursor:
        
        # 2. Insert a record
        insert_record(conn, cursor, NEW_USER_NAME, NEW_USER_EMAIL)
        
        # Optional: Try inserting the same record again to demonstrate the IntegrityError handling
        # insert_record(conn, cursor, NEW_USER_NAME, NEW_USER_EMAIL) 

        # 3. Select and display all records
        display_records(cursor)
        
        # 4. Close the connection
        conn.close()
        print("✅ Database connection closed.")