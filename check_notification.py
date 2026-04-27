import sqlite3
import sys

def show_notification(notification_id=None):
    conn = sqlite3.connect('notifications.db')
    if notification_id is None:
        # Показываем последнее уведомление
        cur = conn.execute('SELECT MAX(id) FROM notifications')
        max_id = cur.fetchone()[0]
        if max_id is None:
            print("Нет уведомлений в базе")
            conn.close()
            return
        notification_id = max_id
        print(f"ID не указан, показываю последнее уведомление (id={notification_id})")
    
    cur = conn.execute('''
        SELECT n.id, t.title, t.body, s.name, n.user_mobile_phone, n.user_email, n.transport, n.status
        FROM notifications n
        JOIN notification_templates t ON n.template_id = t.id
        JOIN info_systems s ON n.information_system_id = s.id
        WHERE n.id = ?
    ''', (notification_id,))
    row = cur.fetchone()
    if row:
        print(f"\nУведомление {row[0]}:")
        print(f"  Шаблон: {row[1]}")
        print(f"  Текст: {row[2]}")
        print(f"  Система: {row[3]}")
        print(f"  Телефон: {row[4]}")
        print(f"  Email: {row[5]}")
        print(f"  Транспорт: {row[6]}")
        print(f"  Статус: {row[7]}")
    else:
        print(f"Уведомление с id={notification_id} не найдено")
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            nid = int(sys.argv[1])
            show_notification(nid)
        except ValueError:
            print("Пожалуйста, укажите числовой ID уведомления")
    else:
        show_notification()