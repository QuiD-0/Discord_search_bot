import discord
import os
import openai

file = data = open('apiKey.txt')
openai.api_key = file.readline()

def search(message):
    msg = message.content.split(' ')
    cmd = " ".join(msg[1:])
    
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=cmd,
    temperature=0.7,
    max_tokens=30,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    
    embed = discord.Embed(title=cmd, color=0x000000)
    embed.add_field(name="Answer", value=response.choices[0].text, inline=True)
    
    return embed, None
    