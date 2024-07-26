import requests
import base64
from .utils import *


def getMapImage(device: str, lat: float, lng: float, date:str):
    '''
    Example path: http://115.146.126.73:7702/api/v1/plan-patrol/map-by-device?DeviceInfo=TB1&Latitude=21.046242&Longitude=105.787002&DateWork=26/07/2024
    '''

    path = f"http://115.146.126.73:7702/api/v1/plan-patrol/map-by-device?DeviceInfo={device}&Latitude={lat}&Longitude={lng}&DateWork={date}"
    try:
        resp = requests.get(path)
    except Exception as e:
        resp = None 
    if (resp != None) and (resp.status_code == 200):
        b64_img_data =  resp.json()['data']['image'][22:]
        image_data_bytes = base64.b64decode(''.join(b64_img_data))
        # img_name = getImageName(resp.json()['time'])
        img_path = f"logs\images\processing\map.png"
        with open(img_path, 'wb+') as image_file:
            image_file.write(image_data_bytes)
        resp_data = {
            "speed_limit": resp.json()['data']['maxSpeed']
        }
    else:
        resp_data = None
    return resp_data
    

def pushDataToServer(data):
    '''
    Data description:
    {
        "Name" : "tên ảnh",
        "Data" : "data:image/png;base64,...",
        "VehicleType" : "car",
        "LicensePlate" : "29-x10 32203",
        "Speed" : 40,
        "SpeedLimit" : 30,
        "Distance" : 100,
        "CaptureDirection" : "Front",
        "RecordTime" : "20/07/2023 16:30:30",
        "Latitude" : 20.998579,
        "Longitude" : 105.813437,
        "RoadAddress" : "nguyen trai",
        "DeviceInfo": "serial number"
    }
    '''
    path = "http://115.146.126.73:7702/api/v1/violation/create"
    resp = requests.post(path, json=data)
    return resp.json()
'''
Usage:
    resp = getMapImage("TB1",21.046242,105.787002,"26/07/2024")
    print(resp)

'''
