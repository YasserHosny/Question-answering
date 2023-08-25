
import os

def get_gpt_key(index):
    match index:
        case 1:
            return os.getenv('OPENAI_API_KEY2')
        case 2:
            return os.getenv('OPENAI_API_KEY3')
        case 3:
            return os.getenv('OPENAI_API_KEY2')
        case _:
            return os.getenv('OPENAI_API_KEY3')
    