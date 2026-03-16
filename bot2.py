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

def main():
    print("🕵️ Бот-шпион запущен и слушает сообщения...")
    print("-" * 50)
    update_id = 0

    while True:
        try:
            # Получаем обновления
            updates = get_updates(offset=update_id)

            if "result" in updates:
                for update in updates["result"]:
                    # Обновляем offset, чтобы не обрабатывать старые сообщения снова
                    update_id = update["update_id"] + 1

                    # Проверяем, есть ли сообщение
                    if "message" in update:
                        message = update["message"]
                        chat_id = message["chat"]["id"]
                        
                        # Получаем username (если есть)
                        username = "None"
                        if "from" in message and "username" in message["from"]:
                            username = "@" + message["from"]["username"]
                        elif "from" in message and "first_name" in message["from"]:
                            username = message["from"]["first_name"]
                            if "last_name" in message["from"]:
                                username += " " + message["from"]["last_name"]
                        
                        # Получаем текст сообщения (если есть)
                        message_text = "💬 [не текстовое сообщение]"
                        if "text" in message:
                            message_text = message["text"]
                        elif "caption" in message:  # Для фото/видео с подписями
                            message_text = f"📝 [подпись к медиа]: {message['caption']}"
                        elif "photo" in message:
                            message_text = "📷 [фото]"
                        elif "video" in message:
                            message_text = "🎥 [видео]"
                        elif "document" in message:
                            message_text = f"📎 [документ]: {message['document']['file_name']}"
                        elif "voice" in message:
                            message_text = "🎤 [голосовое сообщение]"
                        elif "sticker" in message:
                            message_text = "😊 [стикер]"
                        
                        # Выводим информацию в лог
                        log_entry = f"{username} | ID: {chat_id} | {message_text}"
                        print(log_entry)
                        
                        # НЕ ОТПРАВЛЯЕМ НИКАКИХ СООБЩЕНИЙ!

            # Небольшая задержка, чтобы не нагружать сервер
            time.sleep(1)

        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()