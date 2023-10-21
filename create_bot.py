from re import M
import config
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage #хранилище в оперативке

bot = Bot(token=config.TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())