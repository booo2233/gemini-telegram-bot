import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from settings import *
import httpx
import json
from ratelimit import limits, sleep_and_retry
from data_base import *

load_dotenv()
GEMINI_KEY : str = os.getenv("GEMINI_API_KEY")
DEEPGRAM   : str = os.getenv("VOICE_API_KEY")
#genai.configure(api_key=GEMINI_KEY)


url : str =  "https://api.deepgram.com/v1/listen"
url_voice : str = "https://api.deepgram.com/v1/speak?model=aura-luna-en"


with open("system_audio.txt", "r", encoding="utf-8") as f:
 text_sys = f.read()
 

CALLS = 15
RATE_LIMIT = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def voice(file_name, chat_id_messages):
    
    print(file_name)
    headers = {
        "Authorization": f"Token {DEEPGRAM}",
        "Content-Type": "audio/ogg"
    }
    
    # Save the current directory

    
        # Change to the "audio" directory
    os.chdir("audio")

    async with httpx.AsyncClient() as client:
            
            # Open the audio file
            with open(file_name, "rb") as audio_file:
                # Read the file content
                audio_data =  audio_file.read()
            
                # Send the request
                response = await client.post(url, headers=headers, content=audio_data)
                os.chdir("..")
                
                data = response.text
                json_data = json.loads(data)

                text = json_data["results"]["channels"][0]["alternatives"][0]["transcript"]
                
                
                genai.configure(api_key=GEMINI_KEY)

                generation_config : dict = generation_configs_main
                safety_settings : list = safety_settings_main
                
                chat_history_list : list =  get_last_15_messages(chat_id_messages)
                chat_history : str =  "\n".join(chat_history_list)
                text_sys_and_history : str =  text_sys + "\n" + chat_history
                 
                model = genai.GenerativeModel(
                        model_name="gemini-1.5-pro",
                        safety_settings=safety_settings,
                        generation_config=generation_config,
                        system_instruction=text_sys_and_history
                    )
                chat_session = model.start_chat(
                      history=[
                         ]
                    )
#main sand api call
                if text != None:
                   text = text.lower()
  
                   response = chat_session.send_message(text)
                   response = response.text
                   response = response.replace("*", "")
                   voice_text =  response
                   context_history= "user previously asked you :" + str(text) + "\n" + "your Response to users message:" + "```" + str(voice_text) + "```"
                   add_message(chat_id_messages, context_history)
                   if len(voice_text) > 2000:
                     voice_text = voice_text[:2000]
                else:
                    return
               
                  
# Define the headers
                headers = {
                    "Authorization": f"Token {DEEPGRAM}",
                    "Content-Type": "application/json"
                   }

# Define the payload
                payload = {
                   "text": voice_text
                    }

# Make the POST request
                
                response = await client.post(url_voice, headers=headers, json=payload)

# Check if the request was successful
                if response.status_code == 200:
    # Save the response content to a file
                   
                   os.chdir("audio")
                   with open(file_name, "wb") as f:
                     f.write(response.content)
                     os.chdir("..")


                     return file_name
        
                else:
                   print(f"Error: {response.status_code} - {response.text}")





  
#key
  
