import asyncio
import discord
import lol,loa

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

    if message.content.startswith('!help'):
        embed = discord.Embed(title='입력 가능한 명령어', description="추가 문의는 재웅에게!")
        embed.add_field(name="롤 전적", value='!롤 [닉네임]', inline=False)
        embed.add_field(name="로아 정보", value='!로아 [닉네임]', inline=False)
        embed.add_field(name="로아 모험섬", value='!모험섬', inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith('!롤'):
        if len(message.content.split(' '))!=1:
            msg,image = lol.search(message)
            for embed in msg:
                if image:
                    await message.channel.send(embed=embed,file=image)
                    image=None
                else:
                    await message.channel.send(embed=embed)

    if message.content.startswith('!로아'):
        if len(message.content.split(' '))!=1:
            embed,image = loa.search(message)
            await message.channel.send(embed=embed,file=image)

    if message.content.startswith('!모험섬'):
        embed,image=loa.adventure_island()
        await message.channel.send(embed=embed,file=image)


client.run(token)