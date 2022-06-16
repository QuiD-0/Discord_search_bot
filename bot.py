import asyncio
import discord
import lol, loa

client = discord.Client()

file = data = open('token.txt')
token = file.readline()


@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("================")


def who_search(message, s):
    print(f'{message.author}님 {s} 확인')


@client.event
async def on_message(message):
    if message.author.bot:
        return None

    if message.content.startswith('!help'):
        embed = discord.Embed(title='입력 가능한 명령어', description="추가 문의는 재웅에게!")
        # embed.add_field(name="롤 전적", value='!롤 [닉네임]', inline=False)
        embed.add_field(name="로아 정보", value='![닉네임]', inline=False)
        embed.add_field(name="로아 분배금", value='!쌀', inline=False)
        await message.channel.send(embed=embed)

    # if message.content.startswith('!롤'):
    #     who_search(message, '롤 전적')
    #     if len(message.content.split(' ')) != 1:
    #         msg, image = lol.search(message)
    #         for embed in msg:
    #             if image:
    #                 await message.channel.send(embed=embed, file=image)
    #                 image = None
    #             else:
    #                 await message.channel.send(embed=embed)

    if message.content.startswith('!쌀'):
        who_search(message, '쌀')
        if len(message.content.split(' ')) != 1:
            embed, image = loa.calc(message)
            await message.channel.send(embed=embed, file=image)


    elif message.content.startswith('!'):
        who_search(message, '로아 전적')
        embed, image = loa.search(message)
        await message.channel.send(embed=embed, file=image)


client.run(token)
