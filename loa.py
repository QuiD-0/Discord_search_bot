import asyncio
import discord
import requests
from bs4 import BeautifulSoup
import urllib.request

def search(message):
    urllib.request.urlretrieve("https://upload3.inven.co.kr/upload/2021/01/27/bbs/i8293549818.png", "explain.png")
    image = discord.File("explain.png", filename="image.png")

    channel = message.channel
    a=message.content.split(' ') # a=['!안녕','다음','텍스트']
    nickname=a[1]
    url = 'https://loawa.com/char/'+nickname
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content.decode('utf-8','replace')
        soup = BeautifulSoup(html, 'html.parser')
        try :
            name=soup.find_all('span',{'class':'badge badge-pill bg-theme-8 text-theme-1 tfs14 w500'})
            info=soup.find_all('span',{'class':'text-theme-0 tfs14'})
            embed = discord.Embed(title=nickname,url=url, color=0x000000)
            embed.set_thumbnail(url="attachment://image.png")
            for i in range(0,6):
                embed.add_field(name=name[i].get_text(), value=info[i].get_text(), inline=True)
            #각인
            gackin=[]
            gack_active = soup.find('a',{'class':'btn-theme-4 text-right rounded link-theme-4 p-1 active'})
            gackin_tag = soup.find_all('a',{'class':'btn-theme-4 text-right rounded link-theme-4 p-1'})
            gackin.append(gack_active.get_text())
            if gackin_tag:
                for tag in gackin_tag:
                    gackin.append(tag.get_text())
                embed.add_field(name="각인 정보", value='\n'.join(gackin), inline=False)
            else:
                embed.add_field(name="각인 정보", value='각인 없음', inline=False)
            # 수집형 포인트
            points=soup.find('div',{'class':'media pl-2 pb-2 m-0'}).get_text().split()
            point_name=['섬의 마음', '오르페우스의 별', '거인의 심장', '미술품', '모코코', '모험물', '이그네아의증표', '세계수의 잎']
            for i in range(8):
                embed.add_field(name=point_name[i], value=points[i], inline=True)
        except:
            embed = discord.Embed(title='검색 결과 없음', description=nickname)
            image=None
    else : 
        embed = discord.Embed(title='404 NOT FOUND', description='잠시후 다시 시도해주세요.')
        image=None
    
    return embed,image


def adventure_island():
    urllib.request.urlretrieve("https://upload3.inven.co.kr/upload/2021/01/27/bbs/i8293549818.png", "explain.png")
    image = discord.File("explain.png", filename="image.png")

    url='https://loawa.com/'
    response = requests.get(url)
    if response.status_code == 200:
        html = response.content.decode('utf-8','replace')
        soup = BeautifulSoup(html, 'html.parser')
        island=soup.find_all('p',{'class':'text-theme-0 tfs15 p-0 m-0'})
        islands=[]
        desc=[]
        for i in island:
            islands.append(i.find('strong').get_text())
            desc.append(i.find('span').get_text())
        time=soup.select_one('span.text-theme-0.tfs14').get_text()
        embed = discord.Embed(title="오늘의 모험섬",description=time,url=url, color=0x000000)
        embed.set_thumbnail(url="attachment://image.png")
        for i in range(len(islands)):
            embed.add_field(name=islands[i], value=desc[i], inline=False)
        return embed,image