import asyncio
import discord
import requests
from bs4 import BeautifulSoup
def rep(string):
    string=string.replace('\n','')
    return string.strip()

def search(message):
    ans=[]
    channel = message.channel
    a=message.content.split(' ') # a=['!안녕','다음','텍스트']
    nickname='%20'.join(a[1:])
    url = 'https://www.op.gg/summoner/userName='+nickname
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        try : 
            if soup.select_one('#SummonerLayoutContent > div > div > div > div > div > div.TierRank').text:
                TierRank = soup.select_one('#SummonerLayoutContent > div > div > div > div > div > div.TierRank').text
                level=soup.select_one('div.Header > div.Face > div > span').text
                embed = discord.Embed(title=' '.join(a[1:])+" (Lv"+level+")", description=TierRank, color=0x36a4a4, url=url )
                winRatio = soup.select_one('div.WinRatioTitle').text
                winRatio=rep(winRatio)
                embed.add_field(name="최근 전적", value=winRatio, inline=False)
                ans.append(embed)
                try : 
                    if soup.select_one('div.ChampionName').text:
                        ChampionName=soup.select_one('div.ChampionName > a').text
                        ChampionName=rep(ChampionName)
                        kda=soup.select_one('div.Content > div.KDA > div.KDA').text
                        kda=rep(kda)
                        result=soup.select_one('div.GameStats > div.GameResult').text
                        result=rep(result)
                        print(result)
                        if result=='Victory':
                            embed2 = discord.Embed(title='마지막 경기', description=result, color=0xa3cfec) 
                        else:
                            embed2 = discord.Embed(title='마지막 경기', description=result, color=0xe2b6b3) 
                        embed2.add_field(name=ChampionName, value=kda, inline=False)
                        ans.append(embed2)
                except:
                    pass
        except:
            embed = discord.Embed(title='검색 결과 없음', description=' '.join(a[1:]))
            ans.append(embed)
            return ans
    else : 
        print(response.status_code)
    
    return ans