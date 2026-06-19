# Рефакторинг кода Email Клиент Приложение

Приложение `refactoring_email_work.py` - это результат рефакторинга кода `initial_email_work.py`
Приложение предназначено для работы с электронной почтой через протоколы SMTP и IMAP. Предоставляет чистый объектно-ориентированный интерфейс для отправки и получения писем с поддержкой Gmail и других почтовых сервисов.

## Возможности
- Отправка писем: Отправка текстовых писем одному или нескольким получателям
- Получение писем: Чтение писем из почтового ящика
- Фильтрация по теме: Поиск писем по заголовку темы
- Настройка через окружение: Простая настройка с помощью переменных окружения
- Обработка ошибок: Комплексная обработка ошибок с информативными сообщениями
- Совместимость с Gmail: Предварительно настроен для Gmail (можно настроить для других почтовых сервисов)

## Установка

**1. Установите Python**

Убедитесь, что у вас установлен Python 3.8+

```bash
python --version
```
Если Python не установлен: https://www.python.org/downloads/

**2. Клонируйте репозиторий:**
```bash
git clone git@github.com:Oxanchik/code_refactoring_mail.git
cd unit_tests
```

**3. Создайте и активируйте виртуальное окружение (по желанию):**

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**4. Установите зависимости:**
```bash
pip install -r requirements.txt
```

**5. Настройте  переменные окружения**

- **Скопируйте файл-пример**

```bash
cp .env.example .env        # macOS/Linux
copy .env.example .env      # Windows
```

- **Отредактируйте файл `.env` с вашими учетными данными:**

```bash
env
SMTP_SERVER=server_smptp
SMTP_PORT=port_smtp
IMAP_SERVER=server_imap
USER_LOGIN=user_mail
USER_PASSWORD=user_password
```
Примечание: Для Gmail необходимо использовать App Password вместо обычного пароля.

## Использование

```bash
from refactoring_email_work import EmailClient

# Инициализация клиента
client = EmailClient(
    smtp_server="smtp.gmail.com",
    smtp_port="port_smtp",
    imap_server="imap.gmail.com",
    login="your_email@gmail.com",
    password="your_app_password"
)

# Отправка письма
recipients = ['recipient1@example.com', 'recipient2@example.com']
client.send_email(
    recipients=recipients,
    subject="Привет, Мир!",
    message_text="Это тестовое письмо."
)

# Получение письма
email = client.receive_emails(subject_header="Привет, Мир!")
if email:
    print(f"От: {email['From']}")
    print(f"Тема: {email['Subject']}")
```

## Запуск примера

Скрипт включает демонстрацию отправки и получения писем:

```bash
python refactoring_email_work.py
```
