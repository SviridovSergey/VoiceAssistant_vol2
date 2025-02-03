from googlesearch import search
from pyowm import OWM
import pyaudio
import speech_recognition as sr
import os
import vlc
import wikipediaapi
import webbrowser
import traceback
import pyttsx3
import logging
import datetime as t
import math

ttsEngine = pyttsx3.init()
voices = ttsEngine.getProperty('voices')
ttsEngine.setProperty('voices', voices[1].id)
vlc_path = 'D:\\VLC'
os.environ['D:\\VLC'] = os.path.join(vlc_path, 'libvlc.dll')
print(pyaudio.__version__)

class Owner:
    def __init__(self):
        self.name = 'Mark'
        self.home_sity = 'Rostov_on_Don'
        self.launge = 'ru'

def record_and_recognize_audio(microphone, recognizer):
    with microphone:
        recognized_data = ""
        recognizer.adjust_for_ambient_noise(microphone, duration=2)
        try:
            print("Слушаю...")
            audio = recognizer.listen(microphone, timeout=5, phrase_time_limit=5)
            print("Запись завершена, распознавание...")
            recognized_data = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Вы сказали: {recognized_data}")
        except sr.UnknownValueError:
            logging.error("Речь не распознана")
        except sr.RequestError as e:
            logging.error(f"Ошибка сервиса распознавания: {e}")
        except Exception as e:
            logging.error(f"Произошла ошибка: {e}")
        return recognized_data

def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

def play_greetings(*args: tuple):
    greetings = ["Что нужно пидорас???"]
    play_voice_assistant_speech(greetings[0])

def play_farewall_and_quit(*args: tuple):
    farewalls = ["Слава богу.."]
    play_voice_assistant_speech(farewalls[0])
    quit()

def search_on_google(*args: tuple):
    if not args[0]:
        logging.error('Пидорас, повторите пожалуйста')
        return
    search = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search
    webbrowser.get().open(url)
    play_voice_assistant_speech(f'На нахуй')

def search_on_wikipedia(*args: tuple):
    if not args[0]:
        logging.error("Я хуй его")
        return
    search_item = " ".join(args[0])
    wiki = wikipediaapi.Wikipedia('ru')
    wiki_page = wiki.page(search_item)
    try:
        if wiki_page.exists():
            play_voice_assistant_speech('На нахуй')
            webbrowser.get().open(wiki_page.fullurl)
            play_voice_assistant_speech(f'На нахуй + {" ".join(wiki_page.summary.split(".")[:2])}')
        else:
            play_voice_assistant_speech(f'Я хуй его {search_item}. Но вот что высрал Google')
            url = "https://google.com/search?q=" + search_item
            webbrowser.get().open(url)
    except Exception as e:
        logging.error('Я хуй его')
        traceback.print_exc()
        return

def search_in_youtube(*args: tuple):
    if not args[0]:
        logging.error('Я хуй его')
        return
    search_item = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_item
    webbrowser.get().open(url)
    play_voice_assistant_speech('На нахуй')

def get_weather(*args: tuple):
    city_name = Owner().home_sity
    try:
        weather_api_key = '8850cd265a828cad781036fa7a54f26c'
        if not weather_api_key:
            logging.error('Я хуй его')
            raise ValueError('Я ХУЙ ЕГО')
        open_weather_map = OWM(weather_api_key)

        weather_manager = open_weather_map.weather_manager()
        obs = weather_manager.weather_at_place(city_name)
        weather = obs.weather

    except Exception as e:
        logging.error(f'Я хуй его {e}')
        play_voice_assistant_speech('Я хуй его')
        traceback.print_exc()
        return

    status = weather.detailed_status
    temp = weather.temperature('celsius')["temp"]
    wind_speed = weather.wind()["speed"]
    pressure = int(weather.pressure["press"] / 1.333)

    logging.info(f"Погода в {city_name}:\n * Статус: {status}\n * Скорость ветра (m/s): {wind_speed}\n * Температура (°C): {temp}\n * Давление (mm Hg): {pressure}")

    play_voice_assistant_speech(f"Это {status} в {city_name}")
    play_voice_assistant_speech(f"Пидр, температура в {temp} °C")
    play_voice_assistant_speech(f"Пидр, скорость ветра в {wind_speed} m/s")
    play_voice_assistant_speech(f"Пидр, давление в {pressure} mm Hg")

def get_time(*args: tuple):
    time = t.datetime.now().time()
    logging.info(f"Хуйло текущее время: {time}")
    play_voice_assistant_speech(f"Хуйло текущее время: {time}")

def calc(*args: tuple):
    if not args[0]:
        logging.error("Пидорас, введи выражение для вычисления")
        play_voice_assistant_speech("Пидорас, введи выражение для вычисления")
        return

    expression = " ".join(args[0])

    try:
        result = eval(expression, {"__builtins__": None}, {"math": math})
        logging.info(f"Результат вычисления: {result}")
        play_voice_assistant_speech(f"Результат: {result}")
    except Exception as e:
        logging.error(f"Ошибка при вычислении: {e}")
        play_voice_assistant_speech("Пидорас, я не могу это посчитать")

def opera_open_first_window(*args: tuple):
    if not args:
        logging.error("Пидорас, укажи сайт для открытия")
        play_voice_assistant_speech("Пидорас, укажи сайт для открытия")
        return

    opera_path = {'windows': 'C:\\Path\\To\\Opera\\opera.exe'}  # Укажите правильный путь к Opera
    try:
        webbrowser.register('opera', None, webbrowser.BackgroundBrowser(opera_path['windows']))
    except Exception as e:
        logging.error("Слышь хуйлан ен получилось в опере зарегаться")

    quest = " ".join(args[0])
    if not quest.startswith(('http://', 'https://')):
        quest = f'https://{quest}'

    try:
        webbrowser.get('opera').open(quest)
        logging.info(f'Ща открою пидорас')
        play_voice_assistant_speech(f'Ща открою пидорас')
    except Exception as e:
        logging.error(f"Я не смог открыть его, хуйло ебанное, по причине {e}")
        play_voice_assistant_speech("Я не смог открыть его, хуйло ебанное")

commands = {
    ("здарова", "ку", "здарова чепушила"): play_greetings,
    ("пока", "пошел нахуй", "пока чепушила"): play_farewall_and_quit,
    ("найди в гугле ", "высри в поисковике"): search_on_google,
    ("включи", "ролик"): search_in_youtube,
    ("че за хуйня", "что это такое"): search_on_wikipedia,
    ("погода", "какая сегодня погода"): get_weather,
    ("время", "сколько времени щас"): get_time,
    ("посчитай", "вычисли"): calc,
    ("браузер", "включи", "опера", "запусти"): opera_open_first_window
}

def exectute_command_with_name(command_name: str, *args: list):
    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
            return
    logging.info("Нашел че ты хотел хуйло")
    play_voice_assistant_speech("повтори че сказал")

if __name__ == '__main__':
    recognizer = sr.Recognizer()
    microphome = sr.Microphone()

    person = Owner()

    while True:
        voice_input = record_and_recognize_audio(microphome, recognizer)
        if voice_input:
            logging.info(f"Ты высрал: {voice_input}")
            voice_input = voice_input.split(" ")
            command = voice_input[0]
            command_opt = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
            exectute_command_with_name(command, command_opt)