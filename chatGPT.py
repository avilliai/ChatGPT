# -*- coding: utf-8 -*-
import json
import re

import openai
from PIL.ImageDraw import ImageDraw
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
# Set the API key for the openai module
openai.api_key = "sk-xgW2gvXpecEOLM65sfasfxxt6T3BlbkFJj6foExWiIFyV75CXfpSs"

def GPT(stra,mode=1):
    # Use the GPT-3 model to generate text
    print('yourSTR:'+stra)
    prompt = stra
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        temperature=0.5,
    )

    # Print the generated text

    str0 = str(response["choices"][0]["text"])
    str0 = str0.replace('\n\n', '\n')
    if mode==0:
        print(str0)
        return str0
    else:
        s = re.sub(r"(.{50})", "\\1\r\n", str0)
        print(s)



        imageFile = "Config\\back.png"
        tp = Image.open(imageFile)

        font = ImageFont.truetype('Config/SiYuanHeiTiJiuZiXing-Regular-2.ttf', 47)
        draw = ImageDraw.Draw(tp)
        draw.text((190, 799), s, (12, 0, 6), font=font)



        tp.save("pictures\\reply.png")

        return 'pictures\\reply.png'

def chatBack(str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=str,
        temperature=0.6,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    #print(type(response))
    #print((response.get("choice")))
    #print(response)
    #print('------------------------')
    print((response["choices"][0]["text"]))

    return response["choices"][0]["text"]
    #print((dica.get("choice"))[0].get("text"))
    #return str(response["choices"][0])

if __name__ == '__main__':
    chatBack('hello,请为我总结Alan Watts的哲学观点')