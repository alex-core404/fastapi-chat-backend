# language: python
import json
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected: {websocket.client.host}:{websocket.client.port}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"Client disconnected: {websocket.client.host}:{websocket.client.port}")

    async def broadcast(self, message: str, sender: WebSocket | None = None):
        """
        Отправляем message (строка, заранее сериализованный JSON) всем подключённым,
        но пропускаем sender (если он указан).
        """
        print(f"Broadcasting message: {message}")
        for connection in list(self.active_connections):  # list() чтобы безопасно мутировать внутри цикла
            if sender is not None and connection is sender:
                continue  # не отправляем обратно тому, кто послал
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message to {connection.client.host}:{connection.client.port}: {e}")
                self.disconnect(connection)

manager = ConnectionManager()

async def handle_websocket_messages(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # текст от клиента
            # Формируем стандартный JSON-объект сообщения
            msg = {
                "from": f"{websocket.client.host}:{websocket.client.port}",
                "text": data,
                "ts": datetime.utcnow().isoformat() + "Z"
            }
            await manager.broadcast(json.dumps(msg), sender=websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"An unexpected error occurred with {websocket.client.host}:{websocket.client.port}: {e}")
        manager.disconnect(websocket)