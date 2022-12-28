from pytz import timezone
from datetime import datetime
import urllib.request
from collections import defaultdict

import discord
import requests
from bs4 import BeautifulSoup
from lxml import etree

shorcut = defaultdict()
shorcut["전서협"] = "전국서머너홍보협회"

file = data = open('loaOpenApiKey.txt')
apiKey = file.readline()


def search(message):
    channel = message.channel
    a = message.content.split('!')  # a=['!안녕','다음','텍스트']
    nickname = a[1]
    if nickname in shorcut.keys():
        nickname = shorcut[nickname]

    url = 'https://developer-lostark.game.onstove.com/armories/characters/'+ nickname + '/profiles'
    profiles = requests.get(url, headers={'accept': 'application/json',
                                          'authorization': 'bearer '+ apiKey})
    
    url = 'https://developer-lostark.game.onstove.com/armories/characters/'+ nickname + '/engravings'
    engravings = requests.get(url, headers={'accept': 'application/json',
                                          'authorization': 'bearer '+ apiKey})
    
    url = 'https://developer-lostark.game.onstove.com/armories/characters/'+ nickname + '/collectibles'
    collectibles = requests.get(url, headers={'accept': 'application/json',
                                          'authorization': 'bearer '+ apiKey})
    
    characterUrl = 'https://lostark.game.onstove.com/Profile/Character/' + nickname
    
    res = profiles.json()
    gackins = engravings.json()
    points = collectibles.json()
    
    try:
        urllib.request.urlretrieve(res['CharacterImage'], "explain.png")
        image = discord.File("explain.png", filename="image.png")
    except:
        image = None
    
    if profiles.status_code == 200:
        try:
            # 레벨
            level = res['CharacterLevel']
            embed = discord.Embed(title= "Level."+ str(level) + " " + str(nickname), url=characterUrl, color=0x3366ff)
            # 아이템 레벨
            itemLevel = res['ItemMaxLevel']
            embed.add_field(name="아이템 레벨", value=itemLevel, inline=True)
            # 클래스
            userClass = res['CharacterClassName']
            embed.add_field(name="클래스", value=userClass, inline=True)
            # 길드
            guild = res['GuildName']
            embed.add_field(name="길드", value=guild, inline=True)
            # 서버
            server = res['ServerName']
            embed.add_field(name="서버", value=server, inline=True)
            # 영지
            town = res['TownName']
            embed.add_field(name="영지", value=town, inline=True)
            # 원정대
            fellowship = res['ExpeditionLevel']
            embed.add_field(name="원정대", value=fellowship, inline=True)
            final_gackin = []
            for gackin in gackins['Effects']:
                final_gackin.append(gackin['Name'])
            embed.add_field(name="각인 효과", value='\n'.join(final_gackin), inline=True)
    
             # 기본 특성
            status = {}
            for stat in res['Stats']:
                if(stat['Type'] in ["치명","특화","신속"]):
                    status[stat['Type']] = stat['Value']
            embed.add_field(name="기본 특성", value="치명" + " " +status["치명"] + '\n' + "특화" + " " + status["특화"]+ '\n' + "신속" + " " + status["신속"] ,
                            inline=True)
            #공백
            embed.add_field(name="ㅤ", value='ㅤ', inline=False)
            
            # 수집형 포인트
            for collect in points:
                embed.add_field(name=collect['Type'], value=str(collect['Point']) + ' / ' + str(collect['MaxPoint']), inline=True)
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
    if price > 100000:
        embed = discord.Embed(title='너무 큰 금액 아닌가요...?!', description='잠시후 다시 시도해 주세요.')
        image = None
        return embed, image;
    four = price * 0.6478
    eight = price * 0.7556
    image = discord.File("explain.png", filename="image.png")
    embed = discord.Embed(title="분배금 쌀먹", color=0x000000)
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name="4인 기준",
                    value="입찰 추천가 : " + str(int(four)) + " 골드" + "\t손익 분기점 : " + str(int(four * 1.1)) + " 골드",
                    inline=False)
    embed.add_field(name="8인 기준",
                    value="입찰 추천가 : " + str(int(eight)) + " 골드" + "\t손익 분기점 : " + str(int(eight * 1.1)) + " 골드",
                    inline=False)
    return embed, image


def content(flag):
    day = datetime.now(timezone('Asia/Seoul')).weekday()
    word = ["오늘", "내일"]
    if flag:
        day += 1
        day %= 7
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    contents = {0: ["카오스 게이트"], 1: ["필드 보스", "유령선"], 2: [], 3: ["카오스 게이트", "유령선"], 4: ["필드 보스"], 5: ["카오스 게이트", "유령선"],
                6: ["필드 보스", "카오스 게이트", "유령선"]}
    image = discord.File("explain.png", filename="image.png")
    embed = discord.Embed(title=word[flag] + "의 컨텐츠", color=0x000000)
    embed.set_thumbnail(url="attachment://image.png")
    embed.add_field(name=days[day],
                    value="오늘은 컨텐츠가 없어요!" if len(contents[day]) == 0 else ' '.join(contents[day]), inline=False)
    return embed, image


def get_notice():
    image = discord.File("explain.png", filename="image.png")
    embed = discord.Embed(title="최신 공지사항", color=0x000000)
    embed.set_thumbnail(url="attachment://image.png")
    url = 'https://lostark.game.onstove.com/Main'
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
        notices = soup.select('span.main-news__title')
        notices_link = soup.select('a:has(span.main-news__title)')
        print(notices_link)
        for i in range(len(notices)):
            embed.add_field(name=str(i + 1) + "번째 공지",
                            value='[' + str(notices[i].get_text()) + '](' + 'https://lostark.game.onstove.com/' + str(
                                notices_link[i]["href"]) + ')',
                            inline=False)

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
