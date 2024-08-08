import re
import subprocess
import os
import asyncio
import traceback
async def pdf_to_text_func(name_of_pdf:str, chat_id:str) -> str:
    print(name_of_pdf)
    try:
              name_of_text_file  =  f"{chat_id}.txt"
              os.chdir("pdf")
              results =  subprocess.run(["pdftotext", "-layout",name_of_pdf], capture_output=True, text=True, check=True)
    
              print(results.stdout)

              with open(name_of_text_file, "rb+") as  file:
                    file_read = file.read()
                    if b"\x0c" in file_read:
                        print(b"\x0c")
                        file_read = file_read.replace(b"\x0c", b"")
                        file.seek(0)
                        file.write(file_read)
                        file.truncate()  # Ensure the file is truncated to the new length
                        os.remove(name_of_pdf)                       
                        os.chdir("..") 
                        return name_of_text_file   
                    else:
                        
                        os.remove(name_of_pdf)                       
                        os.chdir("..") 
                        return name_of_text_file 
      
               
    except Exception as e:
      traceback.print_exc()
      print(e)
      return 1
  