import discord
import os
import openai
import requests
import json
import io
import base64
from PIL import Image

file = data = open('apiKey.txt')
openai.api_key = file.readline()

file = data = open('kakaoRestApiKey.txt')
kakaoRestApiKey = file.readline()

def search(message):
    msg = message.content.split(' ')
    cmd = " ".join(msg[1:])
    
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=cmd,
    temperature=0.7,
    max_tokens=30,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0)
    
    embed = discord.Embed(title=cmd, color=0x000000)
    embed.add_field(name="Answer", value=response.choices[0].text, inline=True)
    
    return embed, None


def kogpt_api(prompt, max_tokens=64, temperature=0.3, top_p=0.8):

    msg = prompt.content.split(' ')
    cmd = " ".join(msg[1:])

    r = requests.post(
        'https://api.kakaobrain.com/v1/inference/kogpt/generation',
        json = {
            'prompt': cmd,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'n': 1
        },
        headers = {
            'Authorization': 'KakaoAK ' + kakaoRestApiKey,
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    embed = discord.Embed(title=cmd, color=0x000000)
    embed.add_field(name="Answer", value=response['generations'][0]['text'], inline=True)

    return embed, None


async def img(message):
    msg = message.content.split(' ')
    cmd = " ".join(msg[1:])

# 이미지 생성하기 REST API 호출
    response = t2i(cmd, 1)

# 응답의 첫 번째 이미지 생성 결과 출력하기
    result = stringToImage(response.get("images")[0].get("image"), mode='RGB')
    embed = discord.Embed(title= "이미지 변환", color=0x3366ff)
    embed.add_field(name="아이템 레벨", value="result", inline=True)
    result.save('result.png')
    picture = discord.File('result.png')
    await message.channel.send(file=picture)



def t2i(text, batch_size=1):
    r = requests.post(
        'https://api.kakaobrain.com/v1/inference/karlo/t2i',
        json = {
            'prompt': {
                'text': text,
                'batch_size': batch_size
            }
        },
        headers = {
            'Authorization': f'KakaoAK {kakaoRestApiKey}',
            'Content-Type': 'application/json'
        }
    )
    response = json.loads(r.content)
    return response

def stringToImage(base64_string, mode='RGBA'):
    imgdata = base64.b64decode(str(base64_string))
    img = Image.open(io.BytesIO(imgdata)).convert(mode)
    return img

