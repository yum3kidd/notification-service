import sqlite3
conn = sqlite3.connect('notifications.db')
cursor = conn.cursor()
print("\nСистемы\n")
cursor.execute("SELECT * FROM info_systems")
rows = cursor.fetchall()
for row in rows:
    print(row)
print("\nПользователи\n")
cursor.execute("SELECT * FROM mobile_users")
rows = cursor.fetchall()
for row in rows:
    print(row)
print("\nШаблоны\n")
cursor.execute("SELECT * FROM notification_templates")
rows = cursor.fetchall()
for row in rows:
    print(row)
print("\nУведомления\n")
cursor.execute("SELECT * FROM notifications")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()