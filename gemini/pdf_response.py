from dotenv import load_dotenv
import os
import google.generativeai as genai
from settings import *
import asyncio
from ratelimit import limits, sleep_and_retry
import chardet

load_dotenv()

GEMINI_API_KEY : str = os.getenv("GEMINI_API_KEY_IMAGE")


with open("system.txt", "r") as f:
 text_sys = f.read()

CALLS = 15
RATE_LIMIT = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
async def pdf_response_fun(user_text, pdf_text_file_name:str) -> str:

#key
  genai.configure(api_key=GEMINI_API_KEY)

  generation_config : dict = generation_configs_main
  safety_settings : list = safety_settings_main

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=text_sys
  )
  chat_session = model.start_chat(
    history=[
    ]
  )
  os.chdir("pdf")
  


  with open(pdf_text_file_name, "r") as pdf_text:
     pdf_text_read = pdf_text.read()
     pdf_text_read = "PDF ```" + pdf_text_read + "```"

#main sand api call
  if user_text != None:
     os.remove(pdf_text_file_name)
     os.chdir("..")
     text = user_text.lower()
     text = pdf_text_read + text
     response =  chat_session.send_message(text)
     response = response.text
     response = response.replace("*", "")
     return response
