import re

def extract_numbers(text):
    # Define the regular expression pattern
    pattern = r'--start (\d+) --end (\d+)'
    
    # Search for the pattern in the given text
    match = re.search(pattern, text)
    
    # Check if the pattern was found
    if match:
        # Extract the numbers using the capture groups
        start_number = int(match.group(1))
        end_number = int(match.group(2))
        return start_number, end_number
    else:
        # Handle the case where the pattern is not found
        return None, None


def ex(text:str) -> None:
    text_in = text.find(":")
    text    = text[text_in + 1::]
    print(text)

ex("--start 47 --end 67 : fg")
 