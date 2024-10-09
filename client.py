import socket
import threading
import time
import sys
import pyaudio

# Параметры сервера
SERVER_HOST = 'YOUR_IP'  # Укажите IP сервера
SERVER_PORT = YOUR_PORT

# Параметры аудио
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Подключение к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# Ожидаем уведомление от сервера о подключении
connection_message = client_socket.recv(1024).decode()
print(f"Сервер: {connection_message}")

audio = pyaudio.PyAudio()

# Настройка потока для записи
stream_input = audio.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)

# Настройка потока для воспроизведения
stream_output = audio.open(format=FORMAT,
                           channels=CHANNELS,
                           rate=RATE,
                           output=True,
                           frames_per_buffer=CHUNK)

def send_audio():
    """Функция для записи и отправки аудиоданных"""
    while True:
        try:
            data = stream_input.read(CHUNK)
            client_socket.sendall(data)
            time.sleep(0.01)  # Добавляем небольшую задержку для предотвращения перегрузки сети
        except Exception as e:
            print(f"Ошибка при отправке аудио: {e}")
            break

def receive_audio():
    """Функция для получения и воспроизведения аудиоданных"""
    while True:
        try:
            data = client_socket.recv(CHUNK)
            if not data:
                print("Соединение с сервером потеряно.")
                break
            stream_output.write(data)
        except Exception as e:
            print(f"Ошибка при получении аудио: {e}")
            break

# Запуск потоков для отправки и получения аудиоданных
send_thread = threading.Thread(target=send_audio)
receive_thread = threading.Thread(target=receive_audio)

send_thread.start()
receive_thread.start()

send_thread.join()
receive_thread.join()

# Закрытие соединения и аудиопотоков после завершения
client_socket.close()
stream_input.close()
stream_output.close()
audio.terminate()
