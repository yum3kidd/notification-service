## Инициализация тестовых данных

После запуска всех контейнеров выполните одну команду, чтобы создать тестовый шаблон и информационную систему:

cmd
docker exec -it notification_postgres psql -U postgres -d notifications -c "INSERT INTO notification_templates (name, title, body) VALUES ('welcome', 'Добро пожаловать', 'Тестовое сообщение') ON CONFLICT (id) DO NOTHING; INSERT INTO info_systems (name, template_id) SELECT 'Моя система', id FROM notification_templates WHERE name='welcome' ON CONFLICT (id) DO NOTHING;"

После этого можно отправлять POST-запросы на /api/notify с template_id=1 и information_system_id=1.

Проверка статуса уведомления

cmd
docker exec -it notification_postgres psql -U postgres -d notifications -c "SELECT id, status FROM notifications;"
