import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Токен с правами "Товары" и "Сообщения", который вы создали ранее
VK_TOKEN = os.environ.get("VK_TOKEN", "ВАШ_ТОКЕН_СЮДА")
# ID вашего сообщества (число без минуса, например: 219764146)
GROUP_ID = os.environ.get("GROUP_ID", "ВАШ_GROUP_ID")

@app.route('/get_products', methods=['POST'])
def get_products():
    data = request.json or {}
    # GPTunneL будет присылать поисковый запрос (например, "ручка")
    query = data.get('query', '')
    
    url = "https://api.vk.com/method/market.get"
    params = {
        "owner_id": f"-{GROUP_ID}",  # Минус обязателен для сообществ
        "q": query,
        "count": 5,  # Максимум 5 товаров для ответа
        "access_token": VK_TOKEN,
        "v": "5.199"
    }
    
    try:
        response = requests.get(url, params=params).json()
        
        if 'response' in response and 'items' in response['response']:
            items = response['response']['items']
            if not items:
                return jsonify({"answer": "По вашему запросу ничего не найдено. Попробуйте спросить иначе."})
            
            result_text = "Вот что мы нашли в каталоге:\n"
            for item in items:
                title = item.get('title', 'Без названия')
                price = item.get('price', {}).get('text', 'Цена не указана')
                result_text += f"• {title} — {price}\n"
                
            return jsonify({"answer": result_text})
        else:
            return jsonify({"answer": "Не удалось получить данные из каталога. Возможно, произошла ошибка."})
            
    except Exception as e:
        return jsonify({"answer": f"Ошибка при запросе к ВКонтакте: {str(e)}"})

@app.route('/health', methods=['GET'])
def health():
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)