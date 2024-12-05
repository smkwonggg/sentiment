import discord
import re
from discord.ext import commands
import csv
import os
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

# Set up file or read existing file
file_path = 'discordtext.csv'

# initial state of bot
bot_token = '  '
count = 0 

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Analyzing Sentiments"))  # Set presence
    print(f'Logged in as {bot.user}')


@bot.event
async def on_message(message):

    global count
    user_id = message.author.id

    if user_id == bot.user:
        return  # Ignore messages from the bot itself
    
    if ((user_id != bot.user) and (count == 0)):
        count += 1
        await message.channel.send('早晨，我係你老豆 (i am online)')

    # Check if the message contains a sentiment score
    match = sentiment_pattern.search(message.content)

    if match:
        sentiment_score = float(match.group(1))  # Extract the sentiment score as a float
        user_text = message.content[:match.start()].strip()  # Get the message text
        language = detect(user_text)
        timestamp = message.created_at
        formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M')

        if language != 'en':
            translator = Translator( from_lang = language, to_lang = "en")
            translation = translator.translate(user_text)
            formatted_message = (str(user_id)+':', translation, sentiment_score,  formatted_timestamp)
        else:
            formatted_message = (str(user_id)+':', user_text, sentiment_score,  formatted_timestamp)

        print(formatted_message)

        with open(file_path, 'a', newline='') as file:        # Open the file in append mode
            default_header = [ 'UID', 'Text', 'Score', 'Time (UTC)']
            writer = csv.writer(file)

            if os.path.getsize(file_path) == 0:
                writer.writerow(default_header)
            writer.writerow(formatted_message)

        print("Data appended successfully.")

    if message.content.lower() == 'hello':# Check if the message content is "hello"
        await message.channel.send('hello')

    # Process commands if you have any
    await bot.process_commands(message)

# Run the bot with your token
bot.run(bot_token)

