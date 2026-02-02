from fastapi import FastAPI, WebSocket
# Импортируем нашу функцию обработки сообщений из соседнего файла
from app.api.websocket import handle_websocket_messages

# Создаем экземпляр FastAPI приложения
app = FastAPI()

# Обычный HTTP-маршрут. Это как "главная страница" нашего API.
# Он отвечает на GET-запросы к корневому URL (например, http://127.0.0.1:8000/)
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Messenger Backend (V0.2 - No Redis Yet)"}

# Маршрут для WebSocket-соединений.
# Когда кто-то пытается подключиться по WebSocket к адресу /ws (например, ws://127.0.0.1:8000/ws)
# FastAPI вызовет эту функцию.
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Передаем управление в нашу функцию handle_websocket_messages,
    # которую мы подробно разобрали в файле app/api/websocket.py
    await handle_websocket_messages(websocket)

# TODO: Здесь мы добавим другие роуты для API, например, для регистрации пользователей,
# авторизации, получения истории сообщений и т.д.
