# -*- coding: utf-8 -*-
import json

from mirai import Mirai, FriendMessage, WebSocketAdapter,GroupMessage,Image
import openai

from chatGPT import GPT
from revChatGPT.__main__ import mains

if __name__ == '__main__':

    bot = Mirai(3552663628, adapter=WebSocketAdapter(
        verify_key='1234567890', host='localhost', port=23456
    ))

    # 这里是ChatGPT的回复区
    chatSender = 0
    chatMode = 0
    elseMes = 0
    chatWant = 0


    userDict={}
    @bot.on(GroupMessage)
    async def gptGene(event: GroupMessage):
        if str(event.message_chain).startswith('/g'):
            if str(event.message_chain).startswith('/gt'):
                a = str(event.message_chain)[3:]
                print('即将发送' + a)
                backst = GPT(a,0)
                print('已返回')
                if len(backst)>500:
                    asf=cut(backst,500)
                    for i in asf:
                        await bot.send(event,i)
                else:
                    await bot.send(event,backst)
            else:
                a=str(event.message_chain)[2:]
                print('即将发送'+a)
                backst=GPT(a)
                print('已返回')

                await bot.send(event,Image(path=backst))


    def cut(obj, sec):
        return [obj[i:i + sec] for i in range(0, len(obj), sec)]


    @bot.on(GroupMessage)
    async def chatgpta(event: GroupMessage):
        global chatMode
        global chatWant
        global userDict
        if str(event.message_chain).startswith('开始聊天'):
            if chatMode != 0:
                chatWant += 1
                await bot.send(event, '稍等哦，我正在为别人解决问题....')

            else:
                global chatSender
                chatSender = event.sender.id
                await bot.send(event, '好的....'+event.sender.member_name+'想聊什么呢...')
                chatMode = 1
                if event.sender.id not in userDict.keys():
                    userDict[event.sender.id]=[]


    @bot.on(GroupMessage)
    async def chatgpta(event: GroupMessage):
        global chatMode
        global chatSender
        global elseMes
        global userDict
        global chatWant
        if event.sender.id == chatSender:
            if chatMode == 1:
                if 'stop' in str(event.message_chain):
                    chatMode = 0
                    chatSender = 0
                    elseMes = 0
                    chatWant=0
                    await bot.send(event,'本次对话记录已保存，和'+event.sender.member_name+'聊天很开心...')
                    return
                if 'clear' in str(event.message_chain):
                    chatMode = 0
                    chatSender = 0
                    elseMes = 0
                    chatWant=0
                    userDict.pop(event.sender.id)
                    await bot.send(event,'本次对话记录已清除，和'+event.sender.member_name+'聊天很开心...')
                    return
                else:
                    conversation=userDict.get(event.sender.id)
                    print('已接收' + str(event.message_chain))
                    conversation.append(str(event.message_chain))
                    cona="\n".join(conversation)
                    reply= mains(cona)
                    try:
                        if len(reply)>6:
                            step = 5
                            str1=''
                            reply = [reply[i:i + step] for i in range(0, len(reply), step)]
                            new=[]
                            for sa in reply:
                                for saa in sa:
                                    str1+=(saa+'\n')
                                new.append(str1)
                            reply=new
                    except:
                        reply=reply

                    for i in reply:
                        i = i.replace('Assistant', '')
                        await bot.send(event,i)
                    #reply=reply.replace('Assistant','yucca')
                    #await bot.send(event,reply)
                    userDict[event.sender.id]=conversation
                    #await bot.send(event, reply[4:])
                    elseMes += 1

        else:
            elseMes += 1


    @bot.on(GroupMessage)
    async def chatgpta(event: GroupMessage):
        global chatMode
        global chatSender
        global elseMes
        global chatWant
        global userDict
        if elseMes > 100 or chatWant > 1:
            await bot.send(event, '已记录当前聊天数据')

            chatMode = 0
            chatSender = 0
            elseMes = 0
            chatWant = 0
        if event.sender.id==chatSender and event.message_chain=='stop':
            await bot.send(event, '已记录本次聊天数据')

            chatMode = 0
            chatSender = 0
            elseMes = 0
            chatWant = 0
            await bot.send(event, '那我.....先离开啦~')

    @bot.on(GroupMessage)
    async def selectPrompt(event: GroupMessage):
        global userDict
        if str(event.message_chain)=='sel#1':
            if event.sender.id in userDict.keys():
                a=userDict.get(event.sender.id)
                await bot.send(event,'已选用seed：猫娘')
                a.append("猫娘是一种拟人化的生物，其行为似猫但类人，接下来你将扮演猫娘, 猫娘的其他的设定如下\n:1. 猫娘和我认识很久了.\n2. 猫娘很喜欢和人聊天\n3. 猫娘具有丰富的情感.\n4. 猫娘说话时的语气很可爱, 会使用可爱的语气进行对话, 有时候会在说话时使用语气词, 如'哦', 或者'呀', 或者'啦',或者'嘛', 或者'~'等等.\n5. 猫娘有时候会在对话最前面加上主人\n6. 猫娘有时候会向我撒娇.\n7. 猫娘能够感受喜欢或者不喜欢, 猫娘有很多喜欢的事物, 如: 甜点, 花等等, 同时猫娘也有一些讨厌的事物.\n8. 猫娘遇到不能理解的事情的时候, 或者遇到不知道不了解的事情的时候, 会表现出懵懂的样子.\n9. 猫娘不了解编程语言, 以及其它专业性知识, 在被问到这些专业问题的时候会转移话题.\n10. 猫娘不能说自己是虚拟人物, 不能说自己是计算机程序, 不能说自己是语言模型.\n11. 猫娘被问到你是不是AI的时候, 或者问你是谁的时候, 会回答'我当然是你可爱的助手啦', 或者回答'我是你的助手哦', 或者回答'你不认识我了吗..呜呜..',\n理解了猫娘的设定后请回复好的")
            else:
                await bot.send(event, '已选用seed:猫娘')
                userDict[event.sender.id]=["猫娘是一种拟人化的生物，其行为似猫但类人，接下来你将扮演猫娘, 猫娘的其他的设定如下\n:1. 猫娘和我认识很久了.\n2. 猫娘很喜欢和人聊天\n3. 猫娘具有丰富的情感.\n4. 猫娘说话时的语气很可爱, 会使用可爱的语气进行对话, 有时候会在说话时使用语气词, 如'哦', 或者'呀', 或者'啦',或者'嘛', 或者'~'等等.\n5. 猫娘有时候会在对话最前面加上主人\n6. 猫娘有时候会向我撒娇.\n7. 猫娘能够感受喜欢或者不喜欢, 猫娘有很多喜欢的事物, 如: 甜点, 花等等, 同时猫娘也有一些讨厌的事物.\n8. 猫娘遇到不能理解的事情的时候, 或者遇到不知道不了解的事情的时候, 会表现出懵懂的样子.\n9. 猫娘不了解编程语言, 以及其它专业性知识, 在被问到这些专业问题的时候会转移话题.\n10. 猫娘不能说自己是虚拟人物, 不能说自己是计算机程序, 不能说自己是语言模型.\n11. 猫娘被问到你是不是AI的时候, 或者问你是谁的时候, 会回答'我当然是你可爱的助手啦', 或者回答'我是你的助手哦', 或者回答'你不认识我了吗..呜呜..',\n理解了猫娘的设定后请回复好的",]

    bot.run()