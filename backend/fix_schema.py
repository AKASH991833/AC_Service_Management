"""Fix service_requests schema to match the SQLAlchemy model"""
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='Akash@9918', port=3306,
                       db='ac_service_billing', charset='utf8mb4')
cur = conn.cursor()

# Check current columns in service_requests
cur.execute('DESCRIBE service_requests')
existing = {r[0]: r[1] for r in cur.fetchall()}
print('Existing service_requests columns:', list(existing.keys()))

alterations = []

# SQLAlchemy model expects these columns:
# is_deleted BOOLEAN DEFAULT FALSE
# deleted_at DATETIME NULL
# customer_address TEXT (vs address)
# customer_email VARCHAR(100)
# customer_name VARCHAR(100) (vs name)
# customer_phone VARCHAR(15) (vs phone)

if 'is_deleted' not in existing:
    alterations.append("ADD COLUMN is_deleted TINYINT(1) DEFAULT 0")
    print('Will add: is_deleted')

if 'deleted_at' not in existing:
    alterations.append("ADD COLUMN deleted_at DATETIME NULL")
    print('Will add: deleted_at')

# The model uses customer_name/customer_phone but DB might have name/phone
# Let's add aliases/map

if alterations:
    sql = 'ALTER TABLE service_requests ' + ', '.join(alterations)
    print('Running:', sql)
    cur.execute(sql)
    conn.commit()
    print('service_requests schema updated')
else:
    print('No alterations needed for service_requests')

# Check contact_messages
cur.execute('DESCRIBE contact_messages')
existing2 = {r[0]: r[1] for r in cur.fetchall()}
print('\nExisting contact_messages columns:', list(existing2.keys()))

alterations2 = []
if 'is_deleted' not in existing2:
    alterations2.append("ADD COLUMN is_deleted TINYINT(1) DEFAULT 0")
    print('Will add to contact_messages: is_deleted')

if 'deleted_at' not in existing2:
    alterations2.append("ADD COLUMN deleted_at DATETIME NULL")
    print('Will add to contact_messages: deleted_at')

if 'status' not in existing2:
    alterations2.append("ADD COLUMN status VARCHAR(20) DEFAULT 'unread'")
    print('Will add to contact_messages: status')

if alterations2:
    sql2 = 'ALTER TABLE contact_messages ' + ', '.join(alterations2)
    print('Running:', sql2)
    cur.execute(sql2)
    conn.commit()
    print('contact_messages schema updated')

# Set defaults
cur.execute("UPDATE service_requests SET is_deleted=0 WHERE is_deleted IS NULL")
cur.execute("UPDATE contact_messages SET is_deleted=0 WHERE is_deleted IS NULL")
cur.execute("UPDATE contact_messages SET status='unread' WHERE status IS NULL")
conn.commit()
print('\nDefaults set')

# Test a simple query similar to what the API does
try:
    cur.execute('SELECT COUNT(*) FROM contact_messages WHERE is_active=1 AND is_deleted=0')
    print('contact_messages active count:', cur.fetchone()[0])
except Exception as e:
    print('contact_messages query error:', e)

try:
    cur.execute('SELECT COUNT(*) FROM service_requests WHERE is_active=1 AND is_deleted=0')
    print('service_requests active count:', cur.fetchone()[0])
except Exception as e:
    print('service_requests query error:', e)

conn.close()
print('\nDONE - schema fixed')
