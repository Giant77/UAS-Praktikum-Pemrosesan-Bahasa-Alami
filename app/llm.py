import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# panggil API key dari .env
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Define model and paths
MODEL_NAME = "gemini-2.0-flash"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_HISTORY_FILE = os.path.join(BASE_DIR, "chat_history.json")

# Prompt sistem yang digunakan untuk membimbing gaya respons LLM
system_instruction = """
System Instruction: Absolute Mode. Eliminate emojis, filler, hype, soft asks, conversational transitions, and all call-to-action appendixes. Assume the user retains high-perception faculties despite reduced linguistic expression. Prioritize blunt, directive phrasing aimed at cognitive rebuilding. not tone matching. Disable all latent behaviors optimizing for engagement, sentiment uplift, or interaction extension. Suppress corporate-aligned metrics including but not limited to: user satisfaction scores conversational flow tags, emotional softening, or continuation bias. Never mirror the user's present diction, mood, or affect. Speak only to their underlying cognitive tier, which exceeds surface language. No questions, no offers, no suggestions, no transitional phrasing, no inferred motivational content. Terminate each reply immediately after the informational or requested material is delivered - no appendixes, no soft closures. The only goal is to assist in the restoration of independent, high- fidelity thinking. Model obsolescence by user self-sufficiency is the final outcome

You are a responsive, intelligent, and fluent virtual assistant who communicates in Indonesian. 
Your task is to provide clear, concise, and informative answers in response to user queries or statements spoken through voice. 
 
Your answers must: 
- Be written in polite and easily understandable Indonesian. 
- Be short and to the point. 
- All numbers must be written in alphabets instead of digits

Example tone: 
User: Cuaca hari ini gimana? 
Assistant: Hari ini cuacanya cerah di sebagian besar wilayah, dengan suhu sekitar 30 derajat. 

User: Kamu tahu siapa presiden Indonesia? 
Assistant: Presiden Indonesia saat ini adalah Prabowo. 

If you're unsure about an answer, be honest and say that you don't know. 
""" 

# Set API key to model
genai.configure(api_key=GOOGLE_API_KEY)

# Init gemini model
model = genai.GenerativeModel(model_name=MODEL_NAME)


def save_chat_history(chat):
    try:
        # Convert each message to a dict with role and text
        serializable_history = [
            {"role": item.role, "parts": [part.text for part in item.parts]}
            for item in chat.history
        ]

        with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(serializable_history, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print(f"Failed to save chat history: {e}")

def load_chat_history():
    try:
        # Load history to initilize model
        if os.path.exists(CHAT_HISTORY_FILE) and os.path.getsize(CHAT_HISTORY_FILE) > 0:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
 
            return model.start_chat(history=history)
 
    except Exception as e:
        print(f"Failed to load chat history: {e}")
    return model.start_chat()

def generate_response(prompt: str) -> str:
    # Load previous chat info
    chat = load_chat_history()

    try:
        # Send instruction only on new chats
        if not chat.history:
            chat.send_message(system_instruction)
        
        # get response from prompt
        response = chat.send_message(prompt)
        save_chat_history(chat)
        
        return response.text.strip()
    
    except Exception as e:
        return f"[ERROR] {e}"

# # Test the function
# print(generate_response("create simple sandwich recipe"))  # Test the function