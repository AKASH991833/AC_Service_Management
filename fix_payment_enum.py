import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv('Desktop_software/.env')
try:
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE invoices MODIFY COLUMN payment_mode ENUM('Cash', 'Card', 'UPI', 'Bank Transfer', 'Cheque', 'Pending') DEFAULT 'Pending'")
    conn.commit()
    print("Database updated successfully")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
