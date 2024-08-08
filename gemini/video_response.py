from ratelimit import limits, sleep_and_retry
import os
import time
from settings import *
import google.generativeai as genai
import asyncio
from dotenv import load_dotenv
from data_base import *

load_dotenv()

key : str = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=key)

#video_file_name = "saysno.mov"


with open("system.txt", "r", encoding="utf-8") as f:
 text_sys = f.read()

CALLS = 15
RATE_LIMIT = 60


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
###--def---####
async def video_response(text:str, video:str, chat_id_messages:str) -> str:
    os.chdir("video")
    print(f"Uploading file...")
    video_file = genai.upload_file(path=video)
    print(f"Completed upload: {video_file.uri}")


    while video_file.state.name == "PROCESSING":
      print('.', end='')
      video_file = genai.get_file(video_file.name)

      if video_file.state.name == "FAILED":
          raise ValueError(video_file.state.name)

      file = genai.get_file(name=video_file.name)
      print(f"Retrieved file '{file.display_name}'")

# Create the prompt.
    os.remove(video)
    os.chdir("..")

# The Gemini 1.5 models are versatile and work with multimodal prompts
    chat_history_list  : list =  get_last_15_messages(chat_id_messages)
    chat_history : str = "\n".join(chat_history_list)
    text_sys_and_history : str =  text_sys + "\n" + chat_history
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      safety_settings=safety_settings_main,
      generation_config=generation_configs_main,
      system_instruction=text_sys_and_history
                              )

# Make the LLM request.
    if text != None:
       print("Making LLM inference request...")
       response =  model.generate_content([video_file, text],
                                  request_options={"timeout": 600})
       return response.text
       response_message  = response.text
       response_message  =  response_message.replace("*","")
       return response_message   
    else:
         
       response =  model.generate_content([video_file],
                                  request_options={"timeout": 600})   
       response_message  = response.text
       response_message  =  response_message.replace("*","")
       return response_message