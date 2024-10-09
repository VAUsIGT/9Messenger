import socket
import threading
import requests

# Функция для получения внешнего IP-адреса
def get_external_ip():
    try:
        external_ip = requests.get('https://api64.ipify.org').text
        return external_ip
    except requests.RequestException:
        return 'Не удалось получить внешний IP'

# Параметры сервера
SERVER_HOST = '0.0.0.0'  # Слушаем на всех интерфейсах
SERVER_PORT = YOUR_PORT

# Создание TCP-сокета для сервера
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)

# Получаем внешний IP
external_ip = get_external_ip()

# Вывод информации о сервере
print(f"Сервер запущен. Подключайтесь по IP {external_ip} и порту {SERVER_PORT}")

clients = []  # Список для хранения всех подключенных клиентов

def handle_client(client_socket):
    """Обработка аудиоданных от клиента и передача другим клиентам"""
    # Отправляем уведомление клиенту о подключении
    client_socket.send("Вы успешно подключились к серверу.".encode())

    while True:
        try:
            # Получаем аудиоданные от клиента
            audio_data = client_socket.recv(1024)
            if not audio_data:
                break

            # Рассылка аудиоданных всем клиентам, кроме отправителя
            for client in clients:
                if client != client_socket:
                    try:
                        client.sendall(audio_data)
                    except:
                        clients.remove(client)  # Удаляем клиента при ошибке
        except Exception as e:
            print(f"Ошибка при обработке клиента: {e}")
            break

    client_socket.close()
    clients.remove(client_socket)  # Удаляем клиента из списка при разрыве соединения

# Ожидание подключений клиентов
while True:
    client_socket, addr = server_socket.accept()
    print(f"Подключился клиент с адреса: {addr}")
    clients.append(client_socket)

    # Запуск обработки клиента в новом потоке
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
