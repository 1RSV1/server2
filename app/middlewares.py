from aiogram import BaseMiddleware
from aiogram.types import TelegramObject 
from typing import Callable, Dict, Any, Awaitable
import app.database.requests as rq
from aiogram.types import Message
import app.keyboards as kb


class Test(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0
        self.rightans = 0
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],) -> Any:
        print(event)
        data['counter'] = self.counter
        data['rightans'] = self.rightans
        await rq.check_user(event.from_user.id)
        if  await rq.check_user(event.from_user.id):
            result = await handler(event, data)
        else:
            await event.answer("Доступ закрыт, но вас могут добавить")
        data['counter'] = self.counter
        data['rightans'] = self.rightans
        print("Действие после обработчика")
        #await event.answer(f"{event.from_user.first_name}. Это действие после обработчика, но до его вывода из функции мидлвари" )
        return result
