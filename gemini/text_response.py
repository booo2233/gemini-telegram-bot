from ratelimit import limits, sleep_and_retry
import httpx
from dotenv import load_dotenv
import os
import google.generativeai as genai
from settings import *
import asyncio
from data_base import *
text_sys : str = ""
load_dotenv()
key = os.getenv("GEMINI_API_KEY")

image_name : str = ""
print(image_name)

with open("system.txt", "r", encoding="utf-8") as f:
 text_sys = f.read()


CALLS = 15
RATE_LIMIT = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def handle_response(text:str, chat_id_messages:int) -> str:
#key
  genai.configure(api_key=key)
  chat_history_list : list =  get_last_15_messages(chat_id_messages)
  chat_history : str =  "\n".join(chat_history_list)
  text_sys_and_history : str =  text_sys + "\n" + chat_history
  

  generation_config : dict = generation_configs_main
  safety_settings : list = safety_settings_main

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
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
     return response


       

