import discord

import loa

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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
        embed = getHelpEmbed()
        await message.channel.send(embed=embed)

    elif message.content.startswith('!쌀') or message.content.startswith('!Tkf'):
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

    elif message.content.startswith('!'):
        who_search(message, '로아 전적')
        embed, image = loa.search(message)
        await message.channel.send(embed=embed, file=image)


def getHelpEmbed():
    embed = discord.Embed(title='입력 가능한 명령어', description="추가 문의는 재웅에게!")
    embed.add_field(name="로아 캐릭터 정보", value='![닉네임]', inline=False)
    embed.add_field(name="로아 분배금", value='!쌀', inline=False)
    embed.add_field(name="오늘의 컨텐츠", value='!오늘', inline=False)
    embed.add_field(name="내일의 컨텐츠", value='!내일', inline=False)
    embed.add_field(name="최신 공지사항", value='!공지', inline=False)
    return embed


client.run(token)
