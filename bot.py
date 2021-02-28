import asyncio
import discord
import lol

client = discord.Client()

file=data = open('token.txt')
token=file.readline()

@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("================")

@client.event
async def on_message(message):
    if message.author.bot:
        return None

    if message.content.startswith('!롤'):
        if len(message.content.split(' '))!=1:
            msg=lol.search(message)
            if msg:
                for embed in msg:
                    await message.channel.send(embed=embed)

    if message.content.startswith('!로아'):
        pass
    

client.run(token)