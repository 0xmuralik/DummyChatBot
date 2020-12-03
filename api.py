import requests

def weather():
    response = requests.get('https://api.openweathermap.org/data/2.5/weather?q=London&appid=038b8b7cf63b79fa7a4f98c4665ed227')
    data=response.json()
    return data['weather'][0]['description']
