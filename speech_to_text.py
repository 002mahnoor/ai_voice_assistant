import speech_recognition as sr
import pyttsx3
import time
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the text-to-speech engine
engine = pyttsx3.init()
speech = sr.Recognizer()

def get_ai_response(text):
    """
    Send text to Groq API and get response.
    """
    try:
        # Using Groq API
        api_key = os.getenv('GROQ_API_KEY')  # Store your Groq API key in .env file
        if not api_key:
            return "Please set up your GROQ_API_KEY in the .env file."

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Prepare the request payload
        data = {
            'model': 'llama-3.3-70b-versatile',  # Updated to current supported model
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful AI assistant engaging in conversation. Keep your responses concise and natural.'
                },
                {
                    'role': 'user',
                    'content': text
                }
            ],
            'temperature': 0.7,
            'max_tokens': 1024
        }

        # Make the API request
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30  # Add timeout
        )

        # Print response for debugging
        print(f"API Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_json = response.json()
            if 'choices' in response_json and len(response_json['choices']) > 0:
                return response_json['choices'][0]['message']['content'].strip()
            else:
                return "Received empty response from API"
        else:
            error_detail = response.json() if response.text else "No error details available"
            print(f"API Error Details: {error_detail}")
            return f"Error: API returned status code {response.status_code}. Please check your API key and try again."

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return "Sorry, there was a network error. Please check your internet connection."
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return "Sorry, received invalid response from the API."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return f"An unexpected error occurred: {str(e)}"

def speak_text(text):
    """Speak the given text using text-to-speech"""
    try:
        print(f"AI Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def record_text():
    while True:
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise... Please wait...")
                speech.adjust_for_ambient_noise(source, duration=2)
                print("\nListening... Speak something!")
                audio = speech.listen(source, timeout=5, phrase_time_limit=10)
                print("Processing speech...")
                
                try:
                    text = speech.recognize_google(audio)
                    print("You said:", text)
                    
                    # Get AI response
                    print("Getting AI response...")
                    ai_response = get_ai_response(text)
                    print("AI response:", ai_response)
                    
                    # Speak the response
                    speak_text(ai_response)
                    
                    # Save conversation to file
                    save_conversation(text, ai_response)
                    
                    return text
                    
                except sr.UnknownValueError:
                    print("Sorry, I couldn't understand what you said. Please try again.")
                except sr.RequestError as e:
                    print(f"Could not request results from speech service; {e}")
                    print("Please check your internet connection and try again.")
                    time.sleep(2)
        except KeyboardInterrupt:
            print("\nStopping the program...")
            return None
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Please try again.")
            time.sleep(2)

def save_conversation(user_text, ai_response):
    """Save the conversation to a file"""
    try:
        with open("conversation_history.txt", "a") as f:
            f.write(f"User: {user_text}\n")
            f.write(f"AI: {ai_response}\n")
            f.write("-" * 50 + "\n")
    except Exception as e:
        print(f"Error saving conversation: {e}")

print("Interactive Speech AI Program")
print("Press Ctrl+C to exit")
print("-" * 50)

# Create a .env file if it doesn't exist
if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write('GROQ_API_KEY=your_groq_api_key_here\n')
    print("Please add your Groq API key to the .env file")

while True:
    try:
        text = record_text()
        if text is None:  # User pressed Ctrl+C
            break
    except KeyboardInterrupt:
        print("\nExiting program...")
        break

print("Program ended. Check conversation_history.txt for the full conversation.")
    


