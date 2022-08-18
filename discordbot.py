import discord
import requests
import os

API_KEY = '4a7fc725f0327e470a62e530c54f2871'
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


API_KEY_2 = '03a6ee4305f247e6bfa5f95c2fc76128'
NEWS_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=03a6ee4305f247e6bfa5f95c2fc76128'
#https://newsapi.org/v2/top-headlines?country={countryName}&apikey={API_KEY_2}

TOKEN = 'MTAwODI5MDI4Njk2NDg0MjU1Nw.GBRldz.ATRXWv7_Qbhv3Zqnjt1_3KncID2k-qHOYcQBLM'
#all you have to change is the token code to move the bot to a different server


client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message=str(message.content)
    channel = str(message.channel.name)
    #print(f'{username}: {user_message} ({channel})')
    if message.author == client.user:
        return 
    if message.channel.name == 'bot-channel':
        weather_message = user_message[9:].lower()
        if user_message.lower() == f'!weather {weather_message}':
            request_url = f"{BASE_URL}?appid={API_KEY}&q={weather_message}"
            response = requests.get(request_url)
            if response.status_code == 200:
                data = response.json()
                weather = data['weather'][0]['description']
                temperature = round((((data["main"]["temp"] - 273.15) * 9/5)+32), 2)
                celsius = round((data["main"]["temp"] - 273.15), 2)
                await message.channel.send(f'City: {weather_message[0].upper() + weather_message[1:]} \nWeather: {weather} \nTemperature: {temperature} Fahrenheit {celsius} Celsius.')
            elif username.lower() == 'bye':
                await message.channel.send(f'See you later {username}!')
                return
            else:
                await message.channel.send(f'Invalid city name. Pleas re-enter the name, {username}')
                print('An error occured1')
        elif user_message.lower() == '!news today':
            request_url_2 = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=03a6ee4305f247e6bfa5f95c2fc76128'
            response_2 = requests.get(request_url_2)
            if response_2.status_code == 200:
                data_2 = response_2.json()
                title = data_2['articles'][0]['title']
                description = data_2['articles'][0]['description']
                await message.channel.send(f"Today's news headline: {title} \nDescription: {description}")
        elif user_message.lower() == '!jason help':
            await message.channel.send('Possible Commands: \n- !weather (cityName)      [displays the weather and the temperature of a city]\n- !news today                      [displays headline news of today in US]')
        else:
            print('An error occured2')
    if user_message.lower() == '!anywhere':
        await message.channel.send('This can be used anywhere!')
        return

client.run(os.environ["DISCORD_TOKEN"])
