import os
from googlesearch import search
from pyowm import OWM
import speech_recognition as sr
import pyttsx3
import wikipediaapi
import webbrowser
import logging
import datetime as t
import simpleaudio as sa
import pyautogui
import time

# Инициализация TTS-движка
ttsEngine = pyttsx3.init()
voices = ttsEngine.getProperty('voices')
ttsEngine.setProperty('voice', voices[1].id)

# Класс пользователя
class Owner:
    def __init__(self):
        self.name = 'Mark'
        self.home_city = 'Rostov_on_Don'
        self.language = 'ru'

# Функция записи и распознавания аудио
def record_and_recognize_audio(microphone, recognizer):
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        try:
            audio = recognizer.listen(microphone, timeout=5)
            recognized_data = recognizer.recognize_google(audio, language="ru-RU")
            logging.info(f"Распознано: {recognized_data}")
        except sr.WaitTimeoutError:
            logging.warning("Таймаут ожидания голоса.")
        except sr.UnknownValueError:
            logging.warning("Голос не распознан.")
        except sr.RequestError as e:
            logging.error(f"Ошибка сервиса распознавания: {e}")
        return recognized_data

# Проигрывание голосового ответа
def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

# Получение абсолютного пути к звуковым файлам
def get_sound_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Директория скрипта
    sounds_dir = os.path.join(script_dir, "sounds")          # Папка с звуками
    return os.path.join(sounds_dir, filename)

# Приветствие
def play_greetings(*args: tuple):
    audio10 = sa.WaveObject.from_wave_file(get_sound_path("Что нужно пидорас.wav"))
    play_obj = audio10.play()
    play_obj.wait_done()

# Прощание и выход
def play_farewell_and_quit(*args: tuple):
    audio7 = sa.WaveObject.from_wave_file(get_sound_path("Слава богу.wav"))
    play_obj = audio7.play()
    play_obj.wait_done()
    quit()

# Калькулятор
def calc(*args: tuple):
    if not args[0]:
        play_voice_assistant_speech("Введите выражение для вычисления")
        return
    
    expression = " ".join(args[0])
    
    try:
        # Открываем приложение "Калькулятор"
        pyautogui.press('win', interval=0.2)  # Нажимаем клавишу Windows
        pyautogui.write('calculator', interval=0.1)  # Вводим "calculator" в поиске
        pyautogui.press('enter', interval=0.5)  # Нажимаем Enter для открытия
        
        # Ждем пару секунд, пока приложение загрузится
        time.sleep(2)
        
        # Вводим математическое выражение
        for char in expression:
            if char.isdigit() or char in "+-*/().":  # Проверяем допустимые символы
                pyautogui.press(char)
                time.sleep(0.1)  # Небольшая задержка между нажатиями
        
        # Выполняем вычисление (нажимаем Enter)
        pyautogui.press('enter')
        
        logging.info(f"Выражение '{expression}' введено в калькулятор.")
        play_voice_assistant_speech(f"Вычисляю {expression}")
    
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        play_voice_assistant_speech("Я не смогла ввести выражение в калькулятор")

# Поиск в Google
def search_on_google(*args: tuple):
    if not args[0]:
        audio4 = sa.WaveObject.from_wave_file(get_sound_path("Пидорас повторите пожалуйста.wav"))
        play_obj = audio4.play()
        play_obj.wait_done()
        return
    search_query = " ".join(args[0])
    url = f"https://www.google.com/search?q={search_query}"
    webbrowser.get().open(url)
    audio1 = sa.WaveObject.from_wave_file(get_sound_path("На нахуй.wav"))
    play_obj = audio1.play()
    play_obj.wait_done()

# Поиск в Wikipedia
def search_on_wikipedia(*args: tuple):
    audio14 = sa.WaveObject.from_wave_file(get_sound_path("я хуй его.wav"))
    if not args[0]:
        play_obj = audio14.play()
        play_obj.wait_done()
        return
    search_item = " ".join(args[0])
    wiki = wikipediaapi.Wikipedia('ru')
    wiki_page = wiki.page(search_item)
    try:
        if wiki_page.exists():
            audio1 = sa.WaveObject.from_wave_file(get_sound_path("На нахуй.wav"))
            play_obj = audio1.play()
            play_obj.wait_done()
            webbrowser.get().open(wiki_page.fullurl)
            play_voice_assistant_speech(wiki_page.summary.split('.')[:2])
        else:
            play_obj = audio14.play()
            play_obj.wait_done()
            url = f"https://google.com/search?q={search_item}"
            webbrowser.get().open(url)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        play_obj = audio14.play()
        play_obj.wait_done()

# Поиск в YouTube
def search_in_youtube(*args: tuple):
    audio1 = sa.WaveObject.from_wave_file(get_sound_path("На нахуй.wav"))
    audio14 = sa.WaveObject.from_wave_file(get_sound_path("я хуй его.wav"))
    if not args[0]:
        play_obj = audio14.play()
        play_obj.wait_done()
        return
    search_query = " ".join(args[0])
    url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.get().open(url)
    play_obj = audio1.play()
    play_obj.wait_done()

# Получение погоды
def get_weather(*args: tuple):
    city_name = Owner().home_city
    audio14 = sa.WaveObject.from_wave_file(get_sound_path("я хуй его.wav"))
    try:
        weather_api_key = '8850cd265a828cad781036fa7a54f26c'
        if not weather_api_key:
            play_obj = audio14.play()
            play_obj.wait_done()
            raise ValueError("Отсутствует API-ключ для OpenWeatherMap")
        owm = OWM(weather_api_key)
        weather_manager = owm.weather_manager()
        observation = weather_manager.weather_at_place(city_name)
        weather = observation.weather
        status = weather.detailed_status
        temp = weather.temperature('celsius')['temp']
        wind_speed = weather.wind()['speed']
        pressure = int(weather.pressure['press'] / 1.333)
        logging.info(f"Погода в {city_name}: Статус: {status}, Температура: {temp}°C, Ветер: {wind_speed} м/с, Давление: {pressure} мм рт.ст.")
        play_voice_assistant_speech(f"Это {status} в {city_name}. Температура {temp} градусов.")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        play_obj = audio14.play()
        play_obj.wait_done()

# Получение текущего времени
def get_time(*args: tuple):
    current_time = t.datetime.now().time()
    audio9 = sa.WaveObject.from_wave_file(get_sound_path("Хуйло время.wav"))
    play_obj = audio9.play()
    play_obj.wait_done()
    play_voice_assistant_speech(f"Текущее время: {current_time}")

# Открытие ссылки в Opera GX
def opera_open_first_window(*args: tuple):
    if not args[0]:
        logging.error("Укажите сайт для открытия")
        play_voice_assistant_speech("Укажите сайт для открытия")
        return
    quest = " ".join(args[0])
    if not quest.startswith(('http://', 'https://')):
        quest = f"http://{quest}"
    try:
        webbrowser.open(quest)
        play_voice_assistant_speech("Ща открою пидорас")
    except Exception as e:
        logging.error(f"Не удалось открыть ссылку: {e}")
        play_voice_assistant_speech("Я не смог открыть его, хуйло ебанное")

# Словарь команд
commands = {
    ("здарова", "ку", "здарова чепушила"): play_greetings,
    ("пока", "пошел нахуй", "пока чепушила"): play_farewell_and_quit,
    ("найди в гугле", "высри в поисковике"): search_on_google,
    ("включи", "ролик"): search_in_youtube,
    ("че за хуйня", "что это такое"): search_on_wikipedia,
    ("погода", "какая сегодня погода"): get_weather,
    ("время", "сколько времени щас"): get_time,
    ("посчитай", "вычисли"): calc,
    ("браузер", "включи", "опера", "запусти"): opera_open_first_window
}

# Выполнение команды
def execute_command_with_name(command_name: str, *args: list):
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
            return
    play_voice_assistant_speech("Нашел че ты хотел хуйло")
    play_voice_assistant_speech("Повтори че сказал")

if __name__ == '__main__':
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    person = Owner()
    while True:
        voice_input = record_and_recognize_audio(microphone, recognizer)
        if voice_input:
            logging.info(f"Ты высрал: {voice_input}")
            voice_input = voice_input.split(" ")
            command = voice_input[0]
            command_opts = [str(input_part) for input_part in voice_input[1:]]
            execute_command_with_name(command, command_opts)