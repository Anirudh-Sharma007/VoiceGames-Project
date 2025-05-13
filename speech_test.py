
import speech_recognition as sr  # For speech recognition
import sys                       # For system-level operations (optional, useful for exit/args)
import time                      # To optionally add timestamps or delays
import os                        # To interact with OS (optional, useful for mic device checks)

def main():
    recognizer = sr.Recognizer()

    # List available microphones
    mic_list = sr.Microphone.list_microphone_names()
    print("Available microphones:")
    for i, mic in enumerate(mic_list):
        print(f"{i}: {mic}")

    # Use default microphone
    with sr.Microphone() as source:
        print("\nAdjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source)
        print("Ready! Start speaking...\n")

        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source)
                print("Recognizing...")

                # Use Google's online speech recognition API
                text = recognizer.recognize_google(audio)
                print(f"🗣️  You said: {text}\n")

            except sr.UnknownValueError:
                print("❌ Could not understand audio\n")
            except sr.RequestError as e:
                print(f"🚫 Could not request results from Google Speech Recognition service; {e}\n")
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                sys.exit(0)

if __name__ == "__main__":
    main()
