import psycopg2
import json
from datetime import datetime

def connect_to_retool():
    return psycopg2.connect(
        host="ep-wandering-firefly-afii3dov-pooler.c-2.us-west-2.retooldb.com",
        database="retool",
        user="retool",
        password="npg_Wui0EmLg6xeA",
        sslmode="require"
    )

def list_retool_tables():
    conn = connect_to_retool()
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    print(tables)
    return tables

def create_wiremock_table():
    conn = connect_to_retool()
    cursor = conn.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS wiremock (
        id SERIAL PRIMARY KEY,
        original_url TEXT NOT NULL,
        operation VARCHAR(50),
        api_details TEXT,
        mock_url TEXT,
        lob VARCHAR(100),
        environment VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    cursor.execute(create_table_query)
    conn.commit()

    cursor.close()
    conn.close()
    print("✅ wiremock table created (or already exists)")

def add_wiremock_id_column():
    """
    Add wiremock_id column to existing wiremock table if it doesn't exist
    """
    conn = connect_to_retool()
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'wiremock' AND table_schema = 'public';
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        # Add wiremock_id column if it doesn't exist
        if 'wiremock_id' not in existing_columns:
            cursor.execute("ALTER TABLE wiremock ADD COLUMN wiremock_id VARCHAR(100);")
            print("✅ Added 'wiremock_id' column to wiremock table")
        
        conn.commit()
        print("✅ Wiremock_id column updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating table structure: {e}")
        conn.rollback()
    
    cursor.close()
    conn.close()
    """
    Add updated_at column to existing wiremock table if it doesn't exist
    """
    conn = connect_to_retool()
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'wiremock' AND table_schema = 'public';
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        # Add updated_at column if it doesn't exist
        if 'updated_at' not in existing_columns:
            cursor.execute("ALTER TABLE wiremock ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")
            print("✅ Added 'updated_at' column to wiremock table")
        
        conn.commit()
        print("✅ Updated_at column updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating table structure: {e}")
        conn.rollback()
    
    cursor.close()
    conn.close()
    """
    Add headers and parameters columns to existing wiremock table if they don't exist
    """
    conn = connect_to_retool()
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'wiremock' AND table_schema = 'public';
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        # Add headers column if it doesn't exist
        if 'headers' not in existing_columns:
            cursor.execute("ALTER TABLE wiremock ADD COLUMN headers TEXT;")
            print("✅ Added 'headers' column to wiremock table")
        
        # Add parameters column if it doesn't exist
        if 'parameters' not in existing_columns:
            cursor.execute("ALTER TABLE wiremock ADD COLUMN parameters TEXT;")
            print("✅ Added 'parameters' column to wiremock table")
        
        conn.commit()
        print("✅ Headers and parameters columns updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating table structure: {e}")
        conn.rollback()
    
    cursor.close()
    conn.close()
    """
    Add LOB and Environment columns to existing wiremock table if they don't exist
    """
    conn = connect_to_retool()
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'wiremock' AND table_schema = 'public';
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        # Add LOB column if it doesn't exist
        if 'lob' not in existing_columns:
            cursor.execute("ALTER TABLE wiremock ADD COLUMN lob VARCHAR(100);")
            print("✅ Added 'lob' column to wiremock table")
        
        # Add Environment column if it doesn't exist
        if 'environment' not in existing_columns:
            cursor.execute("ALTER TABLE wiremock ADD COLUMN environment VARCHAR(50);")
            print("✅ Added 'environment' column to wiremock table")
        
        conn.commit()
        print("✅ Table structure updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating table structure: {e}")
        conn.rollback()
    
    cursor.close()
    conn.close()

def update_mock_url_nullable():
    """
    Update the mock_url column to allow NULL values for existing tables
    """
    conn = connect_to_retool()
    cursor = conn.cursor()
    
    try:
        # Check if the column exists and has NOT NULL constraint
        cursor.execute("""
            SELECT is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'wiremock' 
            AND column_name = 'mock_url' 
            AND table_schema = 'public';
        """)
        result = cursor.fetchone()
        
        if result and result[0] == 'NO':
            # Remove NOT NULL constraint
            cursor.execute("ALTER TABLE wiremock ALTER COLUMN mock_url DROP NOT NULL;")
            conn.commit()
            print("✅ Updated mock_url column to allow NULL values")
        else:
            print("✅ mock_url column is already nullable")
        
    except Exception as e:
        print(f"❌ Error updating mock_url constraint: {e}")
        conn.rollback()
    
    cursor.close()
    conn.close()

def update_operation_nullable():
    """
    Update the operation column to allow NULL values for existing tables
    """
    conn = connect_to_retool()
    cursor = conn.cursor()
    
    try:
        # Check if the column exists and has NOT NULL constraint
        cursor.execute("""
            SELECT is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'wiremock' 
            AND column_name = 'operation' 
            AND table_schema = 'public';
        """)
        result = cursor.fetchone()
        
        if result and result[0] == 'NO':
            # Remove NOT NULL constraint
            cursor.execute("ALTER TABLE wiremock ALTER COLUMN operation DROP NOT NULL;")
            conn.commit()
            print("✅ Updated operation column to allow NULL values")
        else:
            print("✅ operation column is already nullable")
        
    except Exception as e:
        print(f"❌ Error updating operation constraint: {e}")
        conn.rollback()
    
    cursor.close()
    conn.close()

def add_routing_url_column():
    """
    Add routing_url column and make original_url nullable
    """
    conn = connect_to_retool()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'wiremock' AND table_schema = 'public';
        """)
        existing_columns = [row[0] for row in cursor.fetchall()]
        
        if 'routing_url' not in existing_columns:
            cursor.execute("ALTER TABLE wiremock ADD COLUMN routing_url TEXT NOT NULL;")
            print(" Added 'routing_url' column to wiremock table")
        
        cursor.execute("ALTER TABLE wiremock ALTER COLUMN original_url DROP NOT NULL;")
        print(" Made original_url nullable")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Error updating table structure: {e}")
        conn.rollback()
    
    cursor.close()
    conn.close()

def insert_wiremock_data(routing_url, original_url=None, operation=None, api_details=None, mock_url=None, wiremock_id=None, lob=None, environment=None, headers=None, parameters=None):
    """
    Insert data into the wiremock table
    
    Args:
        routing_url (str): The routing URL (mandatory)
        original_url (str, optional): The original URL being mocked
        operation (str, optional): The HTTP operation (GET, POST, PUT, DELETE, etc.)
        api_details (str, optional): JSON string or text containing API details
        mock_url (str, optional): The mock URL created for this endpoint
        wiremock_id (str, optional): Wiremock ID
        lob (str, optional): Line of Business (Policy, Claims, Small Business, etc.)
        environment (str, optional): Environment (Dev, Test, Staging, Prod)
        headers (str, optional): JSON string containing headers
        parameters (str, optional): JSON string containing parameters
    
    Returns:
        int: The ID of the inserted record, or None if insertion failed
    """
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO wiremock (routing_url, original_url, operation, api_details, mock_url, wiremock_id, lob, environment, headers, parameters)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """

        cursor.execute(insert_query, (routing_url, original_url, operation, api_details, mock_url, wiremock_id, lob, environment, headers, parameters))
        inserted_id = cursor.fetchone()[0]
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Data inserted successfully with ID: {inserted_id}")
        return inserted_id
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return None

def get_wiremock_data(wiremock_id=None):
    """
    Retrieve data from the wiremock table
    
    Args:
        wiremock_id (int, optional): Specific ID to retrieve. If None, returns all records.
    
    Returns:
        list: List of dictionaries containing the wiremock data
    """
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        if wiremock_id:
            query = "SELECT id, routing_url, original_url, operation, api_details, mock_url, lob, environment, headers, parameters, wiremock_id, created_at, updated_at FROM wiremock WHERE id = %s;"
            cursor.execute(query, (wiremock_id,))
        else:
            query = "SELECT id, routing_url, original_url, operation, api_details, mock_url, lob, environment, headers, parameters, wiremock_id, created_at, updated_at FROM wiremock ORDER BY created_at DESC;"
            cursor.execute(query)

        rows = cursor.fetchall()
        columns = ['id', 'routing_url', 'original_url', 'operation', 'api_details', 'mock_url', 'lob', 'environment', 'headers', 'parameters', 'wiremock_id', 'created_at', 'updated_at']
        
        result = []
        for row in rows:
            result.append(dict(zip(columns, row)))

        cursor.close()
        conn.close()
        
        return result
        
    except Exception as e:
        print(f"❌ Error retrieving data: {e}")
        if 'conn' in locals():
            cursor.close()
            conn.close()
        return []
    

def update_wiremock_data(id):
    """
    Update the updated_at timestamp for a specific wiremock record
    
    Args:
        id (int): The ID of the record to update
    """
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        update_query = """
        UPDATE wiremock
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """

        cursor.execute(update_query, (id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print(f"✅ Updated record ID {id} with new updated_at timestamp")
        return True
        
    except Exception as e:
        print(f"❌ Error updating data: {e}")
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return False
    

def delete_record(record_id):
    """Delete a record from the wiremock table"""
    try:
        conn = connect_to_retool()
        cursor = conn.cursor()

        cursor.execute("UPDATE wiremock SET mock_url='mock url deleted', wiremock_id=NULL WHERE wiremock_id = %s;", (record_id,))
        # cursor.execute("DELETE FROM wiremock WHERE id = %s;", (record_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        
        return True
        
    except Exception as e:
        print(f"❌ Error deleting record: {e}")
        
        return False


# add_routing_url_column()

# create_wiremock_table()

# # Update existing table to add new columns if needed
# # add_lob_environment_columns()
# # add_headers_parameters_columns()
# # add_updated_at_column()
# add_wiremock_id_column()

# Update existing table to make mock_url nullable
# update_mock_url_nullable()

# list_retool_tables()