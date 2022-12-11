# -*- coding: utf-8 -*-
import json

from mirai import Mirai, FriendMessage, WebSocketAdapter,GroupMessage,Image
import openai

from chatGPT import GPT
from revChatGPT.__main__ import mains

if __name__ == '__main__':

    bot = Mirai(3093724179, adapter=WebSocketAdapter(
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
                await bot.send(event, '好的....'+event.sender.member_name+'想问什么呢...')
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
                else:
                    conversation=userDict.get(event.sender.id)
                    print('已接收' + str(event.message_chain))
                    conversation.append(str(event.message_chain))
                    cona="\n".join(conversation)
                    reply= mains(cona)
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

                    for i in reply:
                        i = i.replace('Assistant', 'yucca')
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

        if event.message_chain=='clear':
            await bot.send(event, '已清空聊天数据')
            userDict[event.sender.id]=[]
    bot.run()