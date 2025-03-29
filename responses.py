from random import choice, randint



def get_response(user_input: str) -> str:
    lowered: str= user_input.lower()
    if "task" in lowered:
        return "*Function in work*"
    if "hi" in lowered:
        return "Hello there"
       

