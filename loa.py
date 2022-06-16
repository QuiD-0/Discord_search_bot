import urllib.request

import discord
import requests
from bs4 import BeautifulSoup
from lxml import etree


def search(message):
    urllib.request.urlretrieve("https://upload3.inven.co.kr/upload/2021/01/27/bbs/i8293549818.png", "explain.png")
    image = discord.File("explain.png", filename="image.png")

    channel = message.channel
    a = message.content.split('!')  # a=['!안녕','다음','텍스트']
    nickname = a[1]
    url = 'https://www.mgx.kr/lostark/character/?character_name=' + nickname
    response = requests.get(url, headers={'Content-Type': 'text/html; charset=UTF-8',
                                          'Cookie': '__cflb=0H28vwov4WNATuDxs8akb4z2y1B5zpZC5QPzYxABxeq',
                                          'Accept': '*/*',
                                          'Connection': 'keep-alive',
                                          "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                                          'Accept-Encoding': 'gzip, deflate, br',
                                          'Cache-Control': 'no-cache'})
    if response.status_code == 200:
        html = response.content.decode('utf-8', 'replace')
        soup = BeautifulSoup(html, 'html.parser')
        dom = etree.HTML(str(soup))
        try:
            # 레벨
            level = dom.xpath('//*[@id="character_info"]/div[1]/div[5]/div[2]/text()')
            embed = discord.Embed(title=str(level[0]) + " " + str(nickname), url=url, color=0x000000)
            embed.set_thumbnail(url="attachment://image.png")
            # 아이템 레벨
            itemLevel = dom.xpath('//*[@id="character_info"]/div[1]/div[7]/div[2]/text()')
            embed.add_field(name="아이템 레벨", value=itemLevel[0], inline=True)
            # 클래스
            userClass = dom.xpath('//*[@id="character_info"]/div[1]/div[2]/div[2]/text()')
            embed.add_field(name="클래스", value=userClass[0], inline=True)
            # 길드
            guild = dom.xpath('//*[@id="character_info"]/div[1]/div[3]/div[2]/text()')
            embed.add_field(name="길드", value=guild[0], inline=True)
            # 서버
            server = dom.xpath('//*[@id="character_info"]/div[1]/div[2]/div[3]/text()')
            embed.add_field(name="서버", value=server[0], inline=True)
            # 영지
            town = dom.xpath('//*[@id="character_info"]/div[1]/div[8]/div[2]/text()')
            embed.add_field(name="영지", value=town[0], inline=True)
            # 원정대
            fellowship = dom.xpath('//*[@id="character_info"]/div[1]/div[4]/div[2]/text()')
            embed.add_field(name="원정대", value=fellowship[0], inline=True)
            # 기본 특성
            power = dom.xpath('//*[@id="character_info"]/div[4]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/text()')
            hp = dom.xpath('//*[@id="character_info"]/div[4]/div[2]/div[1]/div[1]/div[2]/div[2]/div[2]/text()')
            embed.add_field(name="기본 특성", value="공격력" + " " + str(power[0]) + '\n' + "최대 생명력" + " " + str(hp[0]),
                            inline=False)
            # 각인
            gackin_name = soup.select('div.carving div.carving_category')
            gackin_level = soup.select('div.carving div.carving_level')
            final_gackin = []
            for i in range(len(gackin_name)):
                gackin = gackin_name[i].get_text() + " " + gackin_level[i].get_text()
                final_gackin.append(gackin)
            embed.add_field(name="각인 효과", value='\n'.join(final_gackin), inline=False)
            # 수집형 포인트
            points = soup.select('div.point_number')
            point_name = ['섬의 마음', '오르페우스의 별', '거인의 심장', '미술품', '모코코', '모험물', '이그네아의증표', '세계수의 잎']
            for i in range(8):
                embed.add_field(name=point_name[i], value=points[i].get_text(), inline=True)
        except:
            embed = discord.Embed(title='무언가... 잘못 됐어요', description='잠시후 다시 시도해 주세요.')
            image = None
    else:
        embed = discord.Embed(title='404 NOT FOUND', description='잠시후 다시 시도해 주세요')
        image = None

    return embed, image


def calc(message):
    a = message.content.split(' ')
    price = float(a[1])
    four = price * 0.6478
    eight = price * 0.7556
    image = discord.File("explain.png", filename="image.png")
    embed = discord.Embed(title="분배금 쌀먹", color=0x000000)
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name="4인 기준", value=str(int(four)) + " 골드", inline=True)
    embed.add_field(name="8인 기준", value=str(int(eight)) + " 골드", inline=True)
    return embed, image


def adventure_island():
    urllib.request.urlretrieve("https://upload3.inven.co.kr/upload/2021/01/27/bbs/i8293549818.png", "explain.png")
    image = discord.File("explain.png", filename="image.png")

    url = 'https://loawa.com/'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content.decode('utf-8', 'replace')
        soup = BeautifulSoup(html, 'html.parser')
        island = soup.find_all('p', {'class': 'text-theme-0 tfs15 p-0 m-0'})
        islands = []
        desc = []
        for i in island:
            islands.append(i.find('strong').get_text())
            desc.append(i.find('span').get_text())
        time = soup.select_one('span.text-theme-0.tfs14').get_text()
        embed = discord.Embed(title="오늘의 모험섬", description=time, url=url, color=0x000000)
        embed.set_thumbnail(url="attachment://image.png")
        for i in range(len(islands)):
            embed.add_field(name=islands[i], value=desc[i], inline=False)
        return embed, image
