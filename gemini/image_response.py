from dotenv import load_dotenv
import os
import google.generativeai as genai
from settings import *
import asyncio
from ratelimit import limits, sleep_and_retry
from data_base import *

load_dotenv()

GEMINI_API_KEY : str = os.getenv("GEMINI_API_KEY_IMAGE")


with open("system.txt", "r", encoding="utf-8") as f:
 text_sys = f.read()

CALLS = 15
RATE_LIMIT = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def image_response(text:str, image_file_name:str, chat_id_messages:str) -> str:
  chat_history_list  : list =  get_last_15_messages(chat_id_messages)
  chat_history : str = "\n".join(chat_history_list)
  text_sys_and_history : str =  text_sys + "\n" + chat_history



  genai.configure(api_key=GEMINI_API_KEY)
  def upload_to_gemini(path, mime_type=None):

   file = genai.upload_file(path, mime_type=mime_type)
   print(f"Uploaded file '{file.display_name}'")
   return file
  
  os.chdir("image")

  files = [
  upload_to_gemini(image_file_name, mime_type="image/jpeg")]

  os.remove(image_file_name)
  os.chdir("..")
  
  
  
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
  
  if text == None:
        response = chat_session.send_message([files[0]], stream=True)
        response.resolve()
        return response.text
   
  else: 
    response = chat_session.send_message([text, files[0]], stream=True)
    response.resolve()
    response_message = response.text
    response_message = response_message.replace("*", "")
    return response_message

          
 