import asyncio

import websockets


async def five_times_echo(websocket: websockets.ServerConnection):
	async for message in websocket:
		for _ in range(5):
			response = f"Сообщение пользователя: {message}"
			await websocket.send(response)

async def main():
	server = await websockets.serve(five_times_echo, "localhost", 8765)
	print("Сервер запущен")
	await server.wait_closed()

asyncio.run(main())