import requests
import time

# Токен бота от @BotFather
TOKEN = "8632804306:AAGgMJ-uOzGDt0VgbOovcSVcCNLfbsfKFGg"
API_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_updates(offset=None):
    """Получаем новые сообщения для бота."""
    url = f"{API_URL}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    """Отправляем сообщение пользователю."""
    url = f"{API_URL}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    requests.get(url, params=params)

def main():
    print("Бот запущен и слушает сообщения...")
    update_id = 0

    while True:
        try:
            # Получаем обновления
            updates = get_updates(offset=update_id)

            if "result" in updates:
                for update in updates["result"]:
                    # Обновляем offset, чтобы не обрабатывать старые сообщения снова
                    update_id = update["update_id"] + 1

                    # Проверяем, есть ли текст в сообщении
                    if "message" in update and "text" in update["message"]:
                        chat_id = update["message"]["chat"]["id"]
                        user_text = update["message"]["text"]

                        print(f"Получено сообщение: {user_text}")

                        # Простая логика: эхо или ответ на команду
                        if user_text == "/start":
                            send_message(chat_id, "Привет! Я простой бот. Напиши мне что-нибудь.")
                        else:
                            send_message(chat_id, f"Ты написал: {user_text}")

            # Небольшая задержка, чтобы не нагружать сервер
            time.sleep(1)

        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()