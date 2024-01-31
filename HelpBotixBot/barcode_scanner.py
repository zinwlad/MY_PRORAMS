# barcode_scanner.py
from logger_config import logger
import io
from pyzbar.pyzbar import decode
from PIL import Image
import csv

def scan_barcode(bot, message, csv_filename):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with Image.open(io.BytesIO(downloaded_file)) as image:
            for obj in decode(image):
                box_id = obj.data.decode('utf-8')
                contents = check_box_number(box_id, csv_filename)
                bot.reply_to(message, contents)
                logger.info(f"Штрихкод {box_id} успешно отсканирован.")
    except Exception as e:
        logger.error(f"Ошибка при сканировании штрихкода: {e}")

def check_box_number(box_id, csv_filename):
    try:
        with open(csv_filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            items = [row['ItemName'] for row in reader if row['BoxID'] == box_id]
            file.seek(0)
            box_name = next((row['BoxName'] for row in reader if row['BoxID'] == box_id), None)
            logger.info(f"BoxID {box_id} проверен в CSV-файле.")
            return f"Коробка '{box_name}' ({box_id})" + (f" содержит: {', '.join(items)}" if items else " пуста.")
    except Exception as e:
        logger.error(f"Ошибка проверки номера коробки {box_id}: {e}")

# Конец barcode_scanner.py
