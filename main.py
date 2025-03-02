import telebot
import pytesseract
from PIL import Image
from io import BytesIO
from deep_translator import GoogleTranslator
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TOKEN = "7501305314:AAEk_YpxaOmCiX5dYw_gKNBiOgWFwm5EUXE"
bot = telebot.TeleBot(TOKEN)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

translator = GoogleTranslator(source="auto", target="en")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Надішли мені фото з текстом, і я його розпізнаю.")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file = bot.download_file(file_info.file_path)

    image = Image.open(BytesIO(file))
    text = pytesseract.image_to_string(image, lang="ukr+eng").strip()

    if not text:
        bot.send_message(message.chat.id, "Не вдалося розпізнати текст.")
        return

    bot.send_message(message.chat.id, f"Розпізнаний текст:\n{text}")

    translated_text = translator.translate(text)
    bot.send_message(message.chat.id, f"Переклад англійською:\n{translated_text}")

    logging.info(f"User: {message.chat.id}, Text: {text}")


bot.polling(none_stop=True)
