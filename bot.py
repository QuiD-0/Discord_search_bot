import discord

import loa
import ai

client = discord.Client()

file = data = open('token.txt')
token = file.readline()


@client.event
async def on_ready():
    # pfp_path = "wallhaven-g7z7ld.jpg"
    # fp = open(pfp_path, 'rb')
    # pfp = fp.read()
    # await client.user.edit(avatar=pfp)

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
        embed.add_field(name="로아 캐릭터 정보", value='![닉네임]', inline=False)
        embed.add_field(name="로아 분배금", value='!쌀', inline=False)
        embed.add_field(name="오늘의 컨텐츠", value='!오늘', inline=False)
        embed.add_field(name="내일의 컨텐츠", value='!내일', inline=False)
        embed.add_field(name="최신 공지사항", value='!공지', inline=False)
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

    elif message.content.startswith('!쌀'):
        who_search(message, '쌀')
        if len(message.content.split(' ')) != 1:
            embed, image = loa.calc(message)
            await message.channel.send(embed=embed, file=image)

    elif message.content.startswith('!오늘'):
        who_search(message, '오늘')
        embed, image = loa.content(0)
        await message.channel.send(embed=embed, file=image)

    elif message.content.startswith('!내일'):
        who_search(message, '내일')
        embed, image = loa.content(1)
        await message.channel.send(embed=embed, file=image)

    elif message.content.startswith('!공지'):
        who_search(message, '공지')
        embed, image = loa.get_notice()
        await message.channel.send(embed=embed, file=image)
        
    elif message.content.startswith('!ai'):
        who_search(message, '로아 전적')
        embed, image = ai.search(message)
        await message.channel.send(embed=embed, file=image)
        
    elif message.content.startswith('!'):
        who_search(message, '로아 전적')
        embed, image = loa.search(message)
        await message.channel.send(embed=embed, file=image)


client.run(token)
