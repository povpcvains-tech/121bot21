import requests
import time
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ===== НАСТРОЙКИ =====
TOKEN = "8632804306:AAGgMJ-uOzGDt0VgbOovcSVcCNLfbsfKFGg"  # твой токен
API_URL = f"https://api.telegram.org/bot{TOKEN}/"

# Настраиваем логирование (чтобы видеть, что происходит)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== СОЗДАЁМ СЕССИЮ С ПОВТОРНЫМИ ПОПЫТКАМИ =====
def create_session():
    """Создаёт сессию с автоматическими повторными попытками при ошибках"""
    session = requests.Session()
    
    # Стратегия повторных попыток
    retry_strategy = Retry(
        total=5,  # максимум 5 попыток
        backoff_factor=2,  # пауза между попытками: 2, 4, 8, ... секунд
        status_forcelist=[429, 500, 502, 503, 504],  # коды ошибок для повторных попыток
        allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]
    )
    
    # Адаптер для HTTPS с нашей стратегией
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    # Таймауты (важно!)
    session.timeout = (10, 30)  # (connect timeout, read timeout)
    
    return session

session = create_session()

# ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
def send_message(chat_id, text, retry=3):
    """Отправляет сообщение с повторными попытками при ошибке"""
    url = API_URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    
    for attempt in range(retry):
        try:
            response = session.post(url, json=data, timeout=(10, 30))
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Ошибка отправки (попытка {attempt+1}/{retry}): {e}")
            if attempt < retry - 1:
                time.sleep(3 * (attempt + 1))  # увеличиваем паузу
            else:
                logger.error(f"Не удалось отправить сообщение после {retry} попыток")
                return None

def get_updates(offset=None):
    """Получает обновления с повторными попытками и таймаутом"""
    url = API_URL + "getUpdates"
    params = {
        "timeout": 60,  # долгий poll (60 секунд)
        "offset": offset,
        "allowed_updates": ["message"]
    }
    
    try:
        # Используем долгий таймаут для polling
        response = session.get(url, params=params, timeout=(10, 70))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.warning("Таймаут при получении обновлений (это нормально при долгом poll)")
        return {"ok": True, "result": []}  # пустой результат, продолжаем
    except Exception as e:
        logger.error(f"Ошибка getUpdates: {e}")
        return None

# ===== ГЛАВНЫЙ ЦИКЛ =====
def main():
    logger.info("Бот запущен. Ожидание сообщений...")
    last_update_id = 0
    
    while True:
        try:
            updates = get_updates(last_update_id + 1)
            
            if updates and updates.get("ok"):
                for update in updates.get("result", []):
                    update_id = update["update_id"]
                    last_update_id = update_id
                    
                    if "message" in update:
                        msg = update["message"]
                        chat_id = msg["chat"]["id"]
                        text = msg.get("text")
                        
                        if text:
                            logger.info(f"Получено сообщение: {text}")
                            
                            # Эхо-ответ
                            reply_text = f"Эхо: {text}"
                            send_message(chat_id, reply_text)
            
            # Небольшая пауза, чтобы не нагружать процессор
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            logger.info("Бот остановлен вручную")
            break
        except Exception as e:
            logger.error(f"Критическая ошибка в главном цикле: {e}")
            # Ждём подольше перед перезапуском цикла
            time.sleep(10)

if __name__ == "__main__":
    main()