import speech_recognition as sr
import queue
import threading

def recognize_speech(recognizer, mic, command_queue):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                print("Listening for commands...")
                audio = recognizer.listen(source)
                # command = recognizer.recognize_google(audio).lower()
                command = recognizer.recognize_sphinx(audio).lower()

                print(f"Recognized command: {command}")
                command_queue.put(command)
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Speech Recognition service error!")

recognizer = sr.Recognizer()
mic = sr.Microphone()
# mic = sr.Microphone(device_index=4)

command_queue = queue.Queue()

speech_thread = threading.Thread(target=recognize_speech, args=(recognizer, mic, command_queue), daemon=True)
speech_thread.start()
