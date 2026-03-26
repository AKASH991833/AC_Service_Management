"""Fix contact_messages - add missing is_active and other columns"""
import pymysql

conn = pymysql.connect(host='localhost', user='root', password='Akash@9918', 
                       port=3306, db='ac_service_billing', charset='utf8mb4')
cur = conn.cursor()

cur.execute('DESCRIBE contact_messages')
existing = [r[0] for r in cur.fetchall()]
print('Current columns:', existing)

missing_cols = []
if 'is_active' not in existing:
    missing_cols.append('ADD COLUMN is_active TINYINT(1) DEFAULT 1')
if 'is_deleted' not in existing:
    missing_cols.append('ADD COLUMN is_deleted TINYINT(1) DEFAULT 0')
if 'deleted_at' not in existing:
    missing_cols.append('ADD COLUMN deleted_at DATETIME NULL')
if 'status' not in existing:
    missing_cols.append("ADD COLUMN status VARCHAR(20) DEFAULT 'unread'")

if missing_cols:
    sql = 'ALTER TABLE contact_messages ' + ', '.join(missing_cols)
    print('Running:', sql)
    cur.execute(sql)
    conn.commit()
    print('Columns added!')
else:
    print('All columns already exist')

cur.execute('UPDATE contact_messages SET is_active=1 WHERE is_active IS NULL')
cur.execute('UPDATE contact_messages SET is_deleted=0 WHERE is_deleted IS NULL')
cur.execute("UPDATE contact_messages SET status='unread' WHERE status IS NULL")
conn.commit()

cur.execute('SELECT COUNT(*) FROM contact_messages WHERE is_active=1 AND is_deleted=0')
count = cur.fetchone()[0]
print('Active messages:', count)

cur.execute("SELECT COUNT(*) FROM contact_messages WHERE status='unread'")
unread = cur.fetchone()[0]
print('Unread messages:', unread)

conn.close()
print('DONE!')
