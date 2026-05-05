from datetime import datetime
from utils.telegram import send_telegram


def log(message, telegram=False):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"[{timestamp}] {message}"

    print(line)

    with open("trades.log", "a", encoding="utf-8") as file:
        file.write(line + "\n")# encoding="utf-8"

    if telegram:
        try:
            send_telegram(message)
        except Exception as e:
            print("Erro Telegram:", e)




# from datetime import datetime


# def log(message):

#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     line = f"[{timestamp}] {message}"

#     print(line)

#     with open("trades.log", "a") as file:
#         file.write(line + "\n")