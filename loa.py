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
            lv_nick=soup.select_one('div.pl-2.pr-2.pt-0.pb-0.m-0 > p > span.bg-theme-8.rounded.shadow-sm.text-theme-1.tfs18 > strong').text
            name=soup.find_all('span',{'class':'badge badge-pill bg-theme-8 text-theme-1 tfs14 w500'})
            info=soup.find_all('span',{'class':'text-theme-0 tfs14'})
            embed = discord.Embed(title=lv_nick,url=url, color=0x000000)
            embed.set_thumbnail(url="attachment://image.png")
            for i in range(0,6):
                embed.add_field(name=name[i].get_text(), value=info[i].get_text(), inline=True)
            
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


        except:
            embed = discord.Embed(title='검색 결과 없음', description=nickname)
            return embed,None

    else : 
        embed = discord.Embed(title='404 NOT FOUND', description='잠시후 다시 시도해주세요.')
        return embed,None
    
    return embed,image