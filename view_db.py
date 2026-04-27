import sqlite3

conn = sqlite3.connect('notifications.db')
cursor = conn.cursor()

# Получаем список всех таблиц
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("=== Таблицы в БД ===")
for table in tables:
    print(table[0])

# Для каждой таблицы выведем количество записей
print("\n=== Количество записей ===")
for table in tables:
    name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {name}")
    count = cursor.fetchone()[0]
    print(f"{name}: {count} записей")

conn.close()