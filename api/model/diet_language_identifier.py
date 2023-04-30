from os import path, getcwd
from typing import Text
import asyncio

from rasa.core import agent


class Interpreter:
    def __init__(self, model_path: Text) -> None:
        if not model_path:
            self._model_path = path.join(getcwd(), "model/assets/diet-lang-identifier-v1.0.0.tar.gz")
        
        self._model_path = model_path
        
    async def load_agent(self) -> agent.Agent:
        interpreter = await agent.load_agent(model_path=self._model_path)
        self._interpreter = interpreter
    
    async def parse(self, text: Text):
        print(f"int type: {type(self._interpreter)}")
        parsed_ = await self._interpreter.parse_message(message_data=text)
        return parsed_['intent']['name']


if __name__ == "__main__":
    interpreter = Interpreter(model_path="C:\\Users\\Ishara\\Desktop\\Projects\\diet-language-identifier\\rasa\\models\\nlu-20230430-210832-quantum-dimension.tar.gz")
    asyncio.run(interpreter.load_agent())
    res = asyncio.run(interpreter.parse(text="hi, how are you?"))
    print(f"----------------------")
    print(type(res))
    print(f"detected lang: {res}")
    print(f"----------------------")
    print("terminating...")
