import discord
import re
from discord.ext import commands
import csv
from langdetect import detect, detect_langs
from translate import Translator



# Set up intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.messages = True  # Enable messages intent
intents.message_content = True  # Enable message content intent (required for reading message content)

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# Regular expression to extract the sentiment score
sentiment_pattern = re.compile(r'\(([-+]?\d*\.?\d+)\)')



# initial state of bot
count = 0 

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Analyzing Sentiments"))  # Set presence
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):
    global count 
    if message.author == bot.user:
        return  # Ignore messages from the bot itself
    

    if ((message.author.id != bot.user) and (count == 0)):
        await message.channel.send('早晨，我係你老豆 (i am online)')
        count += 1

    # Check if the message contains a sentiment score
    match = sentiment_pattern.search(message.content)

    if match:
        sentiment_score = float(match.group(1))  # Extract the sentiment score as a float
        user_text = message.content[:match.start()].strip()  # Get the message text
        language = detect(user_text)

        if language != 'en':
            translator = Translator( from_lang = language, to_lang = "en")
            translation = translator.translate(user_text)
            formatted_message = (translation, sentiment_score)
        else:
            formatted_message = (user_text, sentiment_score)
        print(formatted_message)
    


        # Open the CSV file in append mode
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
        # Write the new data
            writer.writerow(formatted_message)

            print("Data appended successfully.")


    # Check if the message content is "pan"
    if message.content.lower() == 'pan':
        await message.channel.send('pan is gay')

    # Process commands if you have any
    await bot.process_commands(message)

# Run the bot with your token
bot.run('MTMwNjYyNzYwNTczODU1NzQ0MA.GgvPGU.AegXmhdOIUHY8uTvPiZUg73n9eZc7J2X0A5320')

