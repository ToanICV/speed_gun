from datetime import datetime
import base64

def getImageName(timestamp):
    # input: "2024-07-26T10:31:37.2388086+07:00"
    # output: map_240726_103137.png
    date, time = timestamp.split('T')
    year, month, day = date.split('-')
    hour, minute, second, _ = time.split(':')
    second = second.split('.')[0]
    formatted_string = f"map_{year[2:]}{month}{day}_{hour}{minute}{second}.png"
    return formatted_string

def getDate() -> str:
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d/%m/%Y")
    return formatted_date

def imgToBase64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string