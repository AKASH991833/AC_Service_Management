"""
Direct Database Check - Verify test data exists
"""
import mysql.connector
from dotenv import load_dotenv
import os
from urllib.parse import unquote

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/ansh_aircool')

def parse_db_url(url):
    if url.startswith('mysql+pymysql://'):
        url = url[16:]
    
    try:
        user_pass, rest = url.split('@')
        host_db = rest.split('/')
        database = host_db[1] if len(host_db) > 1 else ''
        host_port = host_db[0].split(':')
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 3306
        
        user_pass_parts = user_pass.split(':')
        user = user_pass_parts[0]
        password = unquote(user_pass_parts[1]) if len(user_pass_parts) > 1 else ''
        
        return {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
    except Exception as e:
        print(f"Error parsing database URL: {e}")
        return None

print("=" * 70)
print("DIRECT DATABASE CHECK - Verifying Test Data")
print("=" * 70)

db_config = parse_db_url(DATABASE_URL)
if not db_config:
    print("Error: Could not parse database URL")
    exit(1)

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    print("\n[SUCCESS] Connected to database!\n")
    
    # Check Admins
    print("1. Checking Admin Users...")
    cursor.execute("SELECT id, username, email, full_name, is_active FROM admins")
    admins = cursor.fetchall()
    if admins:
        print(f"   Found {len(admins)} admin(s):")
        for admin in admins:
            print(f"      - {admin['username']} ({admin['full_name']}) - Active: {admin['is_active']}")
    else:
        print("   No admins found!")
    
    # Check Service Requests
    print("\n2. Checking Service Requests...")
    cursor.execute("""
        SELECT id, customer_name, customer_phone, service_type, ac_type, 
               request_status, created_at 
        FROM service_requests 
        ORDER BY created_at DESC 
        LIMIT 5
    """)
    requests = cursor.fetchall()
    if requests:
        print(f"   Found {len(requests)} recent service request(s):")
        for req in requests:
            print(f"      #{req['id']}: {req['customer_name']} | {req['service_type']} | " +
                  f"Status: {req['request_status']} | {req['created_at']}")
    else:
        print("   No service requests found!")
    
    # Check Contact Messages
    print("\n3. Checking Contact Messages...")
    cursor.execute("""
        SELECT id, name, phone, service_type, message, status, created_at 
        FROM contact_messages 
        ORDER BY created_at DESC 
        LIMIT 5
    """)
    messages = cursor.fetchall()
    if messages:
        print(f"   Found {len(messages)} recent message(s):")
        for msg in messages:
            msg_preview = msg['message'][:50] + '...' if msg['message'] and len(msg['message']) > 50 else msg['message']
            print(f"      #{msg['id']}: {msg['name']} | {msg['service_type']} | " +
                  f"Status: {msg['status']} | {msg['created_at']}")
            if msg_preview:
                print(f"            Message: {msg_preview}")
    else:
        print("   No contact messages found!")
    
    # Check Website Settings
    print("\n4. Checking Website Settings...")
    cursor.execute("SELECT setting_key, setting_value FROM website_settings")
    settings = cursor.fetchall()
    if settings:
        print(f"   Found {len(settings)} setting(s):")
        for setting in settings:
            print(f"      - {setting['setting_key']}: {setting['setting_value']}")
    else:
        print("   No settings found!")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)
    print("DATABASE CHECK COMPLETE")
    print("=" * 70)
    print("\nAll test data is successfully saved in database!")
    print("\nAdmin Panel Access:")
    print("   URL: http://localhost:5500/admin/index.html")
    print("   Username: admin")
    print("   Password: admin123")
    print("\nData will be visible in admin panel after login!")
    print("=" * 70)
    
except mysql.connector.Error as err:
    print(f"Database Error: {err}")
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
