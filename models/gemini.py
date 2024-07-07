import os
import google.generativeai as genai
from colorama import Fore, Style


class Model:
    def __init__(self):
        GEMINI_API_KEY=os.getenv('GOOGLE_API_KEY')
        if GEMINI_API_KEY is None:
            raise RuntimeError("Google API key is not defined as GOOGLE_API_KEY env variable")

        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate(self, text, verbose, custom_header=""):
        PROMPT_PREFIX = "Summarize the following git diff for a commit message, omit explanation: \n"

        try:
            response = self.model.generate_content(PROMPT_PREFIX + text)
        except:
            raise RuntimeError("Error in Gemini model")
        
        if custom_header:
            formatted_response = "## " + custom_header + " ##\n\n" + response.text
        else:
            formatted_response = response.text 

        if verbose:
            width = int(os.get_terminal_size().columns)
            header = ">" * 10 + " SUGGESTED COMMIT MESSAGE " + ">" * (width - 36)
            print(Fore.BLUE + header)
            print(Fore.WHITE + formatted_response + Fore.RESET)
        
        return formatted_response
    
    @staticmethod
    def sanitize():
        pass
