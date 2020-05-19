import json
import requests
from bs4 import BeautifulSoup
from math import sin, cos, sqrt, atan2, radians


def requestJson(text):
    accessKey = ""
    analysisCode = "ner"

    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": text,
            "analysis_code": analysisCode
        }
    }
    return requestJson


def get_tag(requestJson):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    res = requests.post(openApiURL, headers={"Content-Type": "application/json; charset=UTF-8"},
                        data=json.dumps(requestJson))
    data = res.json()
    try:
        tag = data['return_object']['sentence'][0]['NE'][0]['type']
    except:
        tag = input
    return tag


API_KEY = ""

def get_geocode(address):
    try:
        api_end_point = "https://maps.googleapis.com/maps/api/geocode/xml?address={}&key={}".format(address, API_KEY)

        response = requests.get(api_end_point)
        html = BeautifulSoup(response.text, "lxml")
        lat = html.select_one("location > lat").get_text()  # 위도
        lng = html.select_one("location > lng").get_text()  #경도

        return float(lat), float(lng)
    except Exception as e:
        print(e)


def get_distance(lat1, lng1, lat2, lng2):    #km 단위
    R = 6373.0
    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    dlon = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))

    distance = R*c
    return distance


def classify_tag(tag, input):
    if "LC" in tag or "OG" in tag:
        place_list.append(input)
        place_list.append(get_geocode(input))
        return place_list

    elif tag == "CV_FOOD":
        food_list.append(input)
        return food_list

    # elif

if __name__ == "__main__":
    input = "연트럴파크"
    place_list = []
    food_list = []
    file_name = './place_name.txt'
    file = open(file_name)
    # print(file.read())
    tag = get_tag(requestJson(input))
    print(classify_tag(tag, input))