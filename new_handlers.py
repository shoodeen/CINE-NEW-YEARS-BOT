import json
import random
from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from text import GREETING, FUNCTIONS, FIRST_CAT, SECOND_CAT, THIRD_CAT, FOURTH_CAT, FIFTH_CAT, FUNCTION_BUTTON, \
    RANDOM_CAT, SEE_MORE, SEE_MORE_BUTTON, NO_MORE_FILMS

router = Router()

with open("data/films_data.json", "r") as file:
    f_data = json.load(file)

films_num = 3
remaining_films = {}


def get_cat(category):
    lower = int(category.split("-")[0])
    higher = int(category.split("-")[1])
    cat_result = [item for item in f_data if higher >= int(item[1]) >= lower]
    random.shuffle(cat_result)

    randoms = random.sample(cat_result, min(films_num, len(cat_result)))
    remaining = [item for item in cat_result if item not in randoms]
    result = ["\n🪄 ".join(randomchik) for randomchik in randoms]

    return result, remaining


def store_remaining_films(user_id, films):
    remaining_films[user_id] = films


def get_random():
    data_copy = f_data[:]
    random.shuffle(data_copy)
    randoms = random.sample(data_copy, min(films_num, len(data_copy)))
    remaining = [item for item in data_copy if item not in randoms]
    result = ["\n".join(randomchik) for randomchik in randoms]

    return result, remaining


@router.message(Command("start"))
async def start_handler(msg: Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=FIRST_CAT),
        types.KeyboardButton(text=SECOND_CAT)
    )
    builder.row(
        types.KeyboardButton(text=THIRD_CAT),
        types.KeyboardButton(text=FOURTH_CAT)
    )
    builder.row(
        types.KeyboardButton(text=FIFTH_CAT),
        types.KeyboardButton(text=RANDOM_CAT)
    )
    builder.row(
        types.KeyboardButton(text=FUNCTION_BUTTON)
    )

    await msg.answer(GREETING, reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(F.text.lower() == FIRST_CAT)
async def first_cat(message: types.Message):
    result, remaining = get_cat(FIRST_CAT)
    for film in result:
        await message.answer(f"🎄🎄🎄\n{film}")

    if remaining:
        store_remaining_films(message.from_user.id, remaining)
        await message.reply(text=SEE_MORE,
                            reply_markup=generate_show_more_button())


@router.message(F.text.lower() == SECOND_CAT)
async def sec_cat(message: types.Message):
    result, remaining = get_cat(SECOND_CAT)
    for film in result:
        await message.answer(f"🎄🎄🎄\n{film}")

    if remaining:
        store_remaining_films(message.from_user.id, remaining)
        await message.reply(text=SEE_MORE,
                            reply_markup=generate_show_more_button())

@router.message(F.text.lower() == THIRD_CAT)
async def sec_cat(message: types.Message):
    result, remaining = get_cat(THIRD_CAT)
    for film in result:
        await message.answer(f"🎄🎄🎄\n{film}")

    if remaining:
        store_remaining_films(message.from_user.id, remaining)
        await message.reply(text=SEE_MORE,
                            reply_markup=generate_show_more_button())

@router.message(F.text.lower() == FOURTH_CAT)
async def sec_cat(message: types.Message):
    result, remaining = get_cat(FOURTH_CAT)
    for film in result:
        await message.answer(f"🎄🎄🎄\n{film}")

    if remaining:
        store_remaining_films(message.from_user.id, remaining)
        await message.reply(text=SEE_MORE,
                            reply_markup=generate_show_more_button())

@router.message(F.text.lower() == FIFTH_CAT)
async def sec_cat(message: types.Message):
    result, remaining = get_cat(FIFTH_CAT)
    for film in result:
        await message.answer(f"🎄🎄🎄\n{film}")

    if remaining:
        store_remaining_films(message.from_user.id, remaining)
        await message.reply(text=SEE_MORE,
                            reply_markup=generate_show_more_button())

@router.message(F.text.lower() == RANDOM_CAT)
async def sec_cat(message: types.Message):
    result, remaining = get_random()
    for film in result:
        await message.answer(f"🎄🎄🎄\n{film}")

    if remaining:
        store_remaining_films(message.from_user.id, remaining)
        await message.reply(text=SEE_MORE,
                            reply_markup=generate_show_more_button())


@router.message(F.text.lower() == FUNCTION_BUTTON)
async def functions_but(message: types.Message):
    await message.reply(FUNCTIONS)

def generate_show_more_button():
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text=SEE_MORE_BUTTON, callback_data="show_more")]])


@router.callback_query(F.data == "show_more")
async def show_more_films(query: CallbackQuery):
    user_id = query.from_user.id

    if user_id in remaining_films and remaining_films[user_id]:
        next_films = remaining_films[user_id][:films_num]
        remaining_films[user_id] = remaining_films[user_id][films_num:]

        for film in next_films:
            film_out = '🪄\n'.join(film)
            await query.message.answer(f"🎄🎄🎄\n{film_out}")

        if remaining_films[user_id]:
            await query.message.answer(text=SEE_MORE, reply_markup=generate_show_more_button())
        else:
            await query.message.answer(NO_MORE_FILMS)
            del remaining_films[user_id]
    else:
        await query.message.answer(NO_MORE_FILMS)

    await query.answer()
