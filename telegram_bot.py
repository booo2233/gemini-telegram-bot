#imports for Application
from data_base import *
from telegram import Update
from telegram.ext import *
from dotenv import load_dotenv
import os
import traceback
from gemini.text_response import *
from gemini.image_response import *
from gemini.video_response import *
from gemini.audio_response import *
from extension.file_extension import *
from pdf_to_text import *
from gemini.pdf_response import *
import logging

logging.basicConfig(format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d [%(filename)s])",
                    datefmt="%d/%m/%Y %I:%M:%S %p",
                    level=logging.ERROR,
                    filename="telegram_logs.log",
                    encoding="utf-8")
# load EVN api key
load_dotenv()

#get api key and bot name
TELEGRAM_API_KEY : str = os.getenv("BOT_TELE_KEY")
TELEGRAM_BOT_NAME : str = "@ai_gemini_bot"


#Commands for the bot
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_user_chat_id = int(update.message.chat_id)
    add_user(new_user_chat_id)
    message = """

    <b>Welcome to My Telegram Bot! Powered by Gemini api from google</b>

    <u>Here are some commands you can use:</u>

    <b>/start</b> - Start the bot and see the welcome message :-).
    <b>/help</b> - Display this help message :).
    <b>/custom</b> - Gives back something random, a sticker, random number.

    <i>Note:</i> only English is supported

    <u>Features:</u>
    - <code>Feature 1</code> - Text: Of course, Text the support and text messages is the Important feature
    - <code>Feature 2</code> - Photos: You can send photos. Make sure to add a caption under the photo that will be the question that you are asking the AI about the photos.
    - <code>Feature 3</code> - Videos: Videos are supported. Because of Telegram limitations, make sure to always send file sizes under 20 megabytes. Also don't forget your caption.
    - <code>Feature 4</code> - Voice messages: Voice messages can be sent, and the AI will respond back with voice messages.
    - <code>Feature 5</code> - PDF: You can send files and ask questions about the PDF file. Make sure to add a caption no context for pdf.

     <u>Contact me:</u>
     For further assistance, contact us at <a href="mailto:bugreportoftelegramb.prescribe452@passfwd.com">bugreportoftelegramb.prescribe452@passfwd.com</a>.
     'My github <a href="https://github.com/booo2233">Click here</a>!
     'this telegram bot project on github <a href="https://github.com/booo2233/bot">Click here</a>!
     
     """


    await update.message.reply_html(message)
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html("""
    
    <b>This is the help screen</b>
    - <code>text</code> - Text: Of course, Text the support and text messages is the Important feature
    - <code>image</code> - Photos: You can send photos. Make sure to add a caption under the photo that will be the question that you are asking the AI about the photos.
    - <code>video</code> - Videos: Videos are supported. Because of Telegram limitations, make sure to always send file sizes under 20 megabytes. Also don't forget your caption.
    - <code>voice</code> - Voice messages: Voice messages can be sent, and the AI will respond back with voice messages only English can be used.
    - <code>PDF</code> - PDF: You can send files and ask questions about the PDF file. Make sure to add a caption.

     <u>Contact me:</u>
     For further assistance, contact us at <a href="mailto:bugreportoftelegramb.prescribe452@passfwd.com">bugreportoftelegramb.prescribe452@passfwd.com</a>.
     
     """)



async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")


# main fun for program
async def telegram_bot(update : Update, context : ContextTypes.DEFAULT_TYPE):
     # message_type Get group type public, private or group chat Second line looks for new text messages in chat
     create_tables()

     
     # text response
     if update.message.text:
              chat_id = int(update.message.chat_id)
              add_user(chat_id)
             
              message_type: str = update.message.chat.type
              text : str = update.message.text
              handle_response_text = asyncio.create_task(handle_response(text, chat_id))
             # cheque if it is group or  private chat
              try:

                response: str = await handle_response_text
              #send message and print(response)
                text  = "user previously asked you :" + str(text) + "\n" + "your Response to users message: " + "```" + str(response) + "```" 
                add_message(chat_id, text)
                await update.message.reply_text(response, parse_mode="Markdown")
              except Exception as e:
                  traceback.print_exc()
                  logging.error(f"error curt while processing text {e}")
                  await update.message.reply_sticker("CAACAgIAAxkBAAIKmmamTsOBEc204qRlnFzze9GjcNj3AALzAANWnb0KahvrxMf6lv41BA")
                  await update.message.reply_text("some Went wrong if you think this is a bug, or if you know more, just email me `bugreportoftelegramb.prescribe452@passfwd.com`")
     elif update.message.photo:
            #Get the image ID
            chat_id = update.message.chat.id
            file = await context.bot.get_file(update.message.photo[-1].file_id)
            file_name = f"{update.message.chat.id}.jpg"
            download_folder = "image"
            #get caption of image
            #await update.message.reply_text(file)
            caption = update.message.caption
            #Download the image
            if caption == None:
                 await update.message.reply_text("No caption Please add a caption and send the image once more")

            else:      
               await file.download_to_drive(custom_path=os.path.join(download_folder, file_name))
               image_name = f"{update.message.chat.id}.jpg"
            
            #Send confirmation
               await update.message.reply_text(f"photo downloaded Successfully we are currently processing your image After proofing the image will be deleted {image_name}" , parse_mode="Markdown")
               print(f"{image_name}")
               try:               
                  image_response_task = asyncio.create_task(image_response(caption, image_name, chat_id))   
                  response_of_image = await image_response_task
              
                  await update.message.reply_text(response_of_image, parse_mode="Markdown")
            
                  message_data_base = "user send photo and ask :" + str(caption) + "\n" + "your Response to users image:" + "```" + str(response_of_image) + "```"  
                  add_message(chat_id, message_data_base)
                  
                  # Get the absolute path of the current script
                  current_file_path = os.path.abspath(__file__)

                 # Get the directory path of the current script
                  current_directory_path = os.path.dirname(current_file_path)
                  os.chdir(current_directory_path)
               except Exception as e:
                  logging.error(f"error curt while processing photos {e}")
                  traceback.print_exc()
                  await update.message.reply_sticker("CAACAgIAAxkBAAIKmmamTsOBEc204qRlnFzze9GjcNj3AALzAANWnb0KahvrxMf6lv41BA")
                  await update.message.reply_text("some Went wrong if you think this is a bug, or if you know more, just email me `bugreportoftelegramb.prescribe452@passfwd.com`")
              
            # video response
     elif update.message.video:
               MAX_FILE_VIDEO_SIZE = 20000
               chat_id = update.message.chat.id
               download_folder_video = "video"
               file_name = update.message.video.file_name
               file_size = update.message.video.file_size
               file_size = file_size/1000
               
               
               if file_size > MAX_FILE_VIDEO_SIZE:
                      logging.info("file size is bigger than 20MB")
                      await update.message.reply_text("""Message form the Developer: Due to Telegram API limitations, bots and user in bot chat are only allowed to upload files up to 20MB source:https://core.telegram.org/bots/api#getfile .i apologize for any inconvenience this may cause.""")

     
               else:
                  file = await context.bot.get_file(update.message.video.file_id)
                  caption_video = update.message.caption 
                 
                  if file_name != None:
                                file_name_ex = update.message.video.file_name.split(".")[-1]
                                video_name = f"{chat_id}.{file_name_ex}"

                               
                                await file.download_to_drive(custom_path=os.path.join(download_folder_video, video_name))
                  else:
                               video_name = f"{chat_id}.mp4"
                               await file.download_to_drive(custom_path=os.path.join(download_folder_video, video_name)) 
                  try:
                     video_response_task = asyncio.create_task(video_response(caption_video, video_name, chat_id))
                     response_of_video = await video_response_task

                     await update.message.reply_text(response_of_video, parse_mode="Markdown")
                     message_data_base = "user send video and ask :" + str(caption_video) + "\n" + "your Response to users video:" + "```" + str(response_of_video) + "```"  
                     add_message(chat_id, message_data_base) 
                                       
                     # Get the absolute path of the current script
                     current_file_path = os.path.abspath(__file__)

                     # Get the directory path of the current script
                     current_directory_path = os.path.dirname(current_file_path)
                     os.chdir(current_directory_path)
                  except Exception as e:
                      logging.error(f"error curt while processing video {e}")
                      traceback.print_exc()
                     # Get the absolute path of the current script
                      current_file_path = os.path.abspath(__file__)

                     # Get the directory path of the current script
                      current_directory_path = os.path.dirname(current_file_path)
                      os.chdir(current_directory_path)
                      await update.message.reply_sticker("CAACAgIAAxkBAAIKmmamTsOBEc204qRlnFzze9GjcNj3AALzAANWnb0KahvrxMf6lv41BA")
                      await update.message.reply_text("some Went wrong if you think this is a bug, or if you know more, just email me `bugreportoftelegramb.prescribe452@passfwd.com`")
       # voice response        
     elif update.message.voice:

            chat_id = update.message.chat.id
            download_folder_audio = "audio"
            
            file = await context.bot.get_file(update.message.voice.file_id)
            audio_name = f"{chat_id}.ogg"
            await file.download_to_drive(custom_path=os.path.join(download_folder_audio, audio_name))
            try:
               voice_telegram = asyncio.create_task(voice(audio_name, chat_id))

               response_audio = await voice_telegram
               os.chdir("audio")
               await update.message.reply_voice(response_audio)
               os.chdir("..")


                                    # Get the absolute path of the current script
               current_file_path = os.path.abspath(__file__)

                     # Get the directory path of the current script
               current_directory_path = os.path.dirname(current_file_path)
               os.chdir(current_directory_path)
            except Exception as e:
               logging.error(f"error curt while processing voice {e}")
               traceback.print_exc()
                     # Get the absolute path of the current script
               current_file_path = os.path.abspath(__file__)

                     # Get the directory path of the current script
               current_directory_path = os.path.dirname(current_file_path)
               os.chdir(current_directory_path)
               await update.message.reply_sticker("CAACAgIAAxkBAAIKmmamTsOBEc204qRlnFzze9GjcNj3AALzAANWnb0KahvrxMf6lv41BA")
               await update.message.reply_text("some Went wrong if you think this is a bug, or if you know more, just email me `bugreportoftelegramb.prescribe452@passfwd.com`")
       # pdf response  
     
     elif update.message.document:
          # get user chat id and name dowload folder
          chat_id = update.message.chat.id
          download_folder_doc : str = "pdf"
          # get file id to dowload
          file_doc = await context.bot.get_file(update.message.document.file_id)
          
          # get the file extension 
          name = name_ex(str(file_doc))
          # look if the file end with .pdf extansion
          if name.endswith(".pdf"):
             MAX_FILE_DOCUMENT_SIZE = 10000
             chat_id = update.message.chat.id
             download_folder_video = "video"
             file_name = update.message.document.file_name
             file_size = update.message.document.file_size
             file_size = file_size/1000

             if  file_size > MAX_FILE_DOCUMENT_SIZE:
                      logging.info("file size is bigger than 10MB pdf")
                      await update.message.reply_text("PDF is to bigger than 10MB")
             else:         
                doc_name : str = f"{chat_id}.pdf"
                await file_doc.download_to_drive(custom_path=os.path.join(download_folder_doc, doc_name))
               
                try:
               # get text for the pdf
                  output_of_pdf_to_text = await pdf_to_text_func(doc_name, chat_id)
                  #look if return val is 1 for error
                  if output_of_pdf_to_text == 1:
                     logging.error(f"error in if == 1 ")
                     await update.message.reply_text("some Went wrong if you think this is a bug, or if you know more, just email me `bugreportoftelegramb.prescribe452@passfwd.com`")
                  else:
                  # let the user know that all is going good
                     await update.message.reply_text("all good")
                     caption_pdf = update.message.caption
                   # send the pdf text and user text to ai asycio task
                     pdf_telegram = asyncio.create_task(pdf_response_fun(caption_pdf ,output_of_pdf_to_text))
                   # call the tack
                     response_pdf = await pdf_telegram
                  # send the response of the ai 
                     await update.message.reply_text(response_pdf, parse_mode="Markdown")
                     current_file_path = os.path.abspath(__file__)

                     # Get the directory path of the current script
                     current_directory_path = os.path.dirname(current_file_path)
                     os.chdir(current_directory_path)
                except UnicodeDecodeError:
                     await update.message.reply_text("The pdf you send was non UTF-8 characters Cannot process this file Try with another file or make sure file is not corrupted")
                     current_file_path = os.path.abspath(__file__)
                     # Get the directory path of the current script
                     current_directory_path = os.path.dirname(current_file_path)
                     os.chdir(current_directory_path)
                     traceback.print_exc()
                     logging.error(f"error in except {e} ")
                except Exception as e:
                     current_file_path = os.path.abspath(__file__)

                     # Get the directory path of the current script
                     current_directory_path = os.path.dirname(current_file_path)
                     os.chdir(current_directory_path)
                     traceback.print_exc()
                     logging.error(f"error in except {e} ")
                     await update.message.reply_text("some Went wrong if you think this is a bug, or if you know more, just email me `bugreportoftelegramb.prescribe452@passfwd.com`")

          else:
               await update.message.reply_text("Document type not supported yet")
               
    
    
     elif update.message.sticker:
           file = await context.bot.get_file(update.message.sticker.file_id)
           #await update.message.reply_text(file)
           
     else:
          await update.message.reply_text("**oops What is said now is not supported yet**", parse_mode="Markdown")
       
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
     print(f"Update {"update"} casued error {context.error}")


def main_func():
    print("strarting....")
    app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
     
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.ALL, telegram_bot))
    
    app.add_error_handler(error)
    print("polling...")
    app.run_polling(poll_interval=0) 

if __name__ == "__main__":
 
      main_func()
