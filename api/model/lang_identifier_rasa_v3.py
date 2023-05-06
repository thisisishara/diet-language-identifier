from os import path, getcwd
from typing import Text
import asyncio

from rasa.core import agent
from rasa.core.agent import Agent


class Interpreter:
    def __init__(self, model_path: Text) -> None:
        if not model_path:
            self._model_path = path.join(getcwd(), "assets/v3/")

        self._model_path = model_path

    async def load_agent(self) -> Agent:
        interpreter_ = await agent.load_agent(model_path=self._model_path)
        return interpreter_

    async def parse(self, text: Text):
        print(f"int type: {type(self._interpreter)}")
        parsed_ = await self._interpreter.parse_message(message_data=text)
        return parsed_["intent"]["name"]


if __name__ == "__main__":
    interpreter = Interpreter(model_path="assets/v2/")
    asyncio.run(interpreter.load_agent())
    res = asyncio.run(interpreter.parse(text="hi, how are you?"))
    print(f"detected lang: {res}")
    print("terminating test...")
