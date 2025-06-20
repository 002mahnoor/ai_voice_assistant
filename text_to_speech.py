import pyttsx3
import time
import os

def init_text_to_speech():
    engine = pyttsx3.init()
    # Get available voices and set to a female voice if available
    voices = engine.getProperty('voices')
    if len(voices) > 1:  # If there's more than one voice, use the second one (usually female)
        engine.setProperty('voice', voices[1].id)
    # Set the speaking rate (default is 200)
    engine.setProperty('rate', 150)
    return engine

def read_text_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def speak_text(engine, text):
    try:
        print(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error speaking text: {e}")

def main():
    print("Text-to-Speech Program")
    print("Press Ctrl+C to exit")
    print("-" * 50)

    # Initialize the text-to-speech engine
    engine = init_text_to_speech()
    
    # Keep track of what we've already read
    last_position = 0
    
    try:
        while True:
            # Read the current contents of the file
            lines = read_text_file("output.txt")
            
            # If there are new lines, read them
            if len(lines) > last_position:
                for line in lines[last_position:]:
                    text = line.strip()
                    if text:  # Only speak non-empty lines
                        speak_text(engine, text)
                last_position = len(lines)
            
            # Wait a bit before checking for new content
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nExiting program...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Program ended.")

if __name__ == "__main__":
    main() 