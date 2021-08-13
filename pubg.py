import asyncio
import discord
import requests
from bs4 import BeautifulSoup
import urllib.request

def search(message):
    urllib.request.urlretrieve("http://static.inven.co.kr/images/img-lnb-pubglogo@2x.png?e3ae9c81afdc85296d68458bec52226b","explain.png")
    image = discord.File("explain.png", filename="image.png")
    channel = message.channel
    a = message.content.split(' ')  # a=['!안녕','다음','텍스트']
    nickname = a[1]
    url = 'https://pubg.op.gg/user/' + nickname
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content.decode('utf-8', 'replace')
        soup = BeautifulSoup(html, 'html.parser')
        try:
            rating=soup.select_one('div.ranked-stats__rating-point')



    else:
        embed = discord.Embed(title='404 NOT FOUND', description='잠시후 다시 시도해주세요.')
        return embed, None

    return embed, image