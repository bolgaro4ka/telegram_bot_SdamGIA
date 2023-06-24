import requests


def remove_commas(string):
    trans_table = {ord("'"): None}
    return string.translate(trans_table)


def get_cheat_image():
    url = "https://5-ege.ru/wp-content/uploads/2012/04/matematika-formuly.jpg"
    response = requests.get(url)
    with open("image1.png", 'wb') as f:
        f.write(response.content)
    return response.content


def get_fox_image():
    url = f"https://randomfox.ca/floof/"
    response = requests.get(url)
    if response:
        return response.json()["image"]


def get_questions_info(count):
    url = f"http://jservice.io/api/random?count={count}"
    response = requests.get(url)
    if response:
        return response.json()


def get_year_info(year):
    url = f"http://numbersapi.com/{year}/year"
    response = requests.get(url)
    if response:
        return response.text
