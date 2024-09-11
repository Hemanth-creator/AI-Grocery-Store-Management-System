import pyodbc

def connect_to_db():
    try:
        conn = pyodbc.connect(
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DESKTOP-746R9QA\SQLEXPRESS;'
            'DATABASE=Grocery_DB;'
            'Trusted_Connection=yes;'
        )
        return conn
    except Exception as e:
        print(f"Error while connecting: {e}")
        return None
    
def read_records(table):
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return dict(rows)
    except Exception as e:
        print(f"Error during SELECT operation: {e}")
    finally:
        conn.close()