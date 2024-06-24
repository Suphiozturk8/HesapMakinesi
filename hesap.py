
import os
from math import sqrt
from typing import Union
from pyrogram import Client, filters
from pyrogram.errors import exceptions
from pyrogram.enums import ParseMode
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup as Keyboard,
    InlineKeyboardButton as Button,
    )

if not os.path.exists("HesapMakinesi.session"):
    API_ID = int(input("\n[?] API_ID'yi girin:\n❯❯ "))
    API_HASH = input("\n[?] API_HASH'ı girin:\n❯❯ ")
    BOT_TOKEN = input("\n[?] BOT_TOKEN'i girin:\n❯❯ ")


def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

clear()


casper_app = Client(
    "HesapMakinesi", 
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)


@casper_app.on_message(filters.command(["start", "help"]))
@casper_app.on_message(filters.regex(r"\b(?:[Cc]al(?:c(?:ulator)?)?|[Hh]esap(?:la(?:mak)?| makinesi)?)\b"))
async def start(_: Client, message: Message) -> None:
    user_id: int = message.from_user.id
    caption: str = "İşleminizi Girin:\n\n|"
    first_name = message.from_user.first_name

    markup: Keyboard = Keyboard([
        [Button("AC", "c"), Button("DEL", "DEL"), Button(first_name, url="https://t.me/BioCasper")], 
        [Button("√", "sqrt("), Button("^", "**"), Button("(", "("), Button(")", ")")],
        [Button("7", "7"), Button("8", "8"), Button("9", "9"), Button("÷", "/")],
        [Button("4", "4"), Button("5", "5"), Button("6", "6"), Button("×", "*")],
        [Button("1", "1"), Button("2", "2"), Button("3", "3"), Button("-", "-")],
        [Button(".", "."), Button("0", "0"), Button("=", "="), Button("+", "+")],
        [Button("- Hesap Makinesini Gizle -", f"d {user_id}")]
    ])

    await message.reply(
        caption,
        reply_markup=markup,
        reply_to_message_id=message.id)


@casper_app.on_callback_query(filters.regex(r"^(c)$"))
async def clear(_: Client, callback: CallbackQuery) -> None:
    user_id: int = callback.from_user.id 
    caption: str = "İşleminizi Girin:\n\n|"
    markup: Keyboard = callback.message.reply_markup

    if int(markup.inline_keyboard[-1][0].callback_data.split()[1]) != user_id:
        return await callback.answer(
            "Bu arayüz sizin için değil!",
            show_alert=True)

    try:
        await callback.edit_message_text(
            caption,
            reply_markup=markup)
    except exceptions.bad_request_400.MessageNotModified:
        await callback.answer(
            "Silinecek bir şey yok!")


@casper_app.on_callback_query(filters.regex(r"^(DEL)$"))
async def rm(_: Client, callback: CallbackQuery):
    user_id: int = callback.from_user.id 
    text: str = callback.message.text
    markup: Keyboard = callback.message.reply_markup

    if int(markup.inline_keyboard[-1][0].callback_data.split()[1]) != user_id:
        return await callback.answer(
            "Bu arayüz sizin için değil!",
            show_alert=True)
    elif text.endswith("|"):
        return await callback.answer(
            "Silinecek bir şey yok!")

    caption: str = text[:-1] if len(text.split("\n")[1]) > 1 else text[:-1] + "|"

    return await callback.edit_message_text(
        caption,
        reply_markup=markup)


@casper_app.on_callback_query(filters.regex(r"^(0|1|2|3|4|5|6|7|8|9)$"))
@casper_app.on_callback_query(filters= lambda _, callback: callback.data in "+**/-sqrt()^.=")
async def _input(_: Client, callback: CallbackQuery) -> None:
    user_id: int = callback.from_user.id
    markup: Keyboard = callback.message.reply_markup.inline_keyboard

    if int(markup[-1][0].callback_data.split()[1]) != user_id:
        return await callback.answer(
            "Bu arayüz sizin için değil!",
            show_alert=True)
    elif callback.data == "=":
        return await callback.answer(
            "Önce bir işlem girin:\n\n|",
            show_alert=True)

    caption: str = f"{callback.message.text.replace('|', '')}{callback.data}"
    markup[-2][-2].callback_data = "result " + caption.split('\n', 1)[-1]

    await callback.edit_message_text(
        caption,
        reply_markup=Keyboard(markup),
        parse_mode=ParseMode.HTML)


@casper_app.on_callback_query(filters.regex(r"^(result)"))
async def _result(_: Client, callback: CallbackQuery) -> None:
    user_id: int = callback.from_user.id
    data: str = callback.data
    markup: Keyboard = callback.message.reply_markup

    if int(markup.inline_keyboard[-1][0].callback_data.split()[1]) != user_id:
        return await callback.answer(
            "Bu arayüz sizin için değil!",
            show_alert=True)

    markup.inline_keyboard[-2][-2].callback_data = "="

    try:
        result: Union[int, float] = eval(data.split(maxsplit=1)[1])
    except ZeroDivisionError:
        return await callback.answer(
            "Sıfıra bölemezsiniz!",
            show_alert=True)
    except SyntaxError:
        return await callback.answer(
            "İşlemi doğru yazdığınızdan emin olun!",
            show_alert=True)

    caption: str = f"İşlem Sonucu:\n\n{result}"
    await callback.edit_message_text(
        caption,
        reply_markup=markup)


@casper_app.on_callback_query(filters.regex(r"^(d )"))
async def d(_: Client, callback: CallbackQuery) -> None:
    user_id: int = callback.from_user.id
    markup: Keyboard = callback.message.reply_markup

    if int(markup.inline_keyboard[-1][0].callback_data.split()[1]) != user_id:
        return await callback.answer(
            "Bu arayüz sizin için değil!",
            show_alert=True)

    await callback.message.delete()

    
if __name__=="__main__":
    print("Bot Aktif...")
    casper_app.run()
