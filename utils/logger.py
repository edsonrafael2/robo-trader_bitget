from datetime import datetime


def log(message):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"[{timestamp}] {message}"

    print(line)

    with open("trades.log", "a") as file:
        file.write(line + "\n")