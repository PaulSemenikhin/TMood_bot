from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON

router: Router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEXICON['invalid_message'])
