from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import json

app = FastAPI()

# Хранилище для активных WebSocket-соединений
connected_clients = set()

# HTML-страница с улучшенным дизайном
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Chat</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Прокрутка без полосы прокрутки */
        #chat::-webkit-scrollbar {
            display: none;
        }
        #chat {
            -ms-overflow-style: none;  /* IE и Edge */
            scrollbar-width: none;  /* Firefox */
        }
        /* Анимация появления сообщений */
        .message {
            animation: fadeIn 0.3s ease-in;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
    <div class="w-full max-w-lg bg-white rounded-lg shadow-lg p-6 flex flex-col h-[80vh]">
        <h1 class="text-2xl font-bold text-gray-800 mb-4 text-center">Чат</h1>
        <div id="chat" class="flex-1 overflow-y-auto p-4 space-y-4">
            <!-- Сообщения будут добавляться сюда -->
        </div>
        <div class="flex gap-2 mt-4">
            <input type="text" id="message" placeholder="Введите сообщение" 
                   class="flex-1 p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <button id="send" onclick="sendMessage()" 
                    class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
                Отправить
            </button>
        </div>
    </div>
    <script>
        const ws = new WebSocket(`ws://${window.location.host}/ws`);
        const chat = document.getElementById('chat');
        const messageInput = document.getElementById('message');

        ws.onmessage = function(event) {
            const msg = JSON.parse(event.data);
            const div = document.createElement('div');
            div.className = 'message max-w-[70%] p-3 rounded-lg ' + 
                            (msg.sender === 'User' ? 'bg-blue-100 ml-auto' : 'bg-gray-200 mr-auto');
            div.innerHTML = `<span class="font-semibold">${msg.sender}:</span> ${msg.text}`;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        };

        function sendMessage() {
            const text = messageInput.value.trim();
            if (text) {
                ws.send(JSON.stringify({ sender: 'User', text: text }));
                messageInput.value = '';
            }
        }

        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            # Рассылаем сообщение всем подключенным клиентам
            for client in connected_clients:
                await client.send_text(json.dumps(message))
    except Exception:
        connected_clients.remove(websocket)