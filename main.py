# -*- coding: utf-8 -*-
import json

from mirai import Mirai, WebSocketAdapter,GroupMessage,Image

from chatGPT import GPT

from revChatGPT.__main__ import configure

if __name__ == '__main__':

    bot = Mirai(3552663628, adapter=WebSocketAdapter(
        verify_key='1234567890', host='localhost', port=23456
    ))
    file = open('Config\\userDict.txt', 'r')
    js = file.read()
    userDict = json.loads(js)


    print('已读取prompt')
    # 这里是ChatGPT的回复区
    chatSender = 0
    chatMode = 0
    elseMes = 0
    chatWant = 0
    learnMode=1


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
                if str(event.sender.id) in userDict.keys():
                    print('存在用户')
                else:
                    print('创建用户')
                    userDict[str(event.sender.id)]=[]


    @bot.on(GroupMessage)
    async def chatgpta(event: GroupMessage):
        global chatMode
        global chatSender
        global elseMes
        global userDict
        global chatWant
        global learnMode
        if event.sender.id == chatSender:
            if chatMode == 1:
                if 'stop' in str(event.message_chain):
                    chatMode = 0
                    chatSender = 0
                    elseMes = 0
                    chatWant=0
                    save()
                    await bot.send(event,'本次对话记录已保存，和'+event.sender.member_name+'聊天很开心...')
                    return
                if 'clear' in str(event.message_chain):
                    chatMode = 0
                    chatSender = 0
                    elseMes = 0
                    chatWant=0
                    del userDict[str(event.sender.id)]
                    save()
                    await bot.send(event,'本次对话记录已清除，和'+event.sender.member_name+'聊天很开心...')
                    return
                if str(event.message_chain) == '记录模式':
                    learnMode = 1
                    await bot.send(event, '已开启记录,接下来的对话将被记录用于生成回复')
                    return
                if '停止记录' in str(event.message_chain) :
                    learnMode = 0
                    await bot.send(event, '已关闭，不再记录对话')
                    return
                else:
                    conversation=userDict.get(str(event.sender.id))
                    print('已接收' + str(event.message_chain))
                    if len(str(event.message_chain))>600:
                        await bot.send(event,'检测到长字符串，自动关闭记录模式')
                        learnMode=0
                    conversation.append(str(event.message_chain))
                    cona="\n".join(conversation)
                    if len(cona)>900:
                        await bot.send(event, '当前语料过长，为保证使用，自动关闭记录模式')
                        learnMode = 0
                    reply= configure(cona)
                    if type(reply)==list:
                        # 对返回的列表进行处理
                        if len(reply)>2:
                            b=[]
                            for issa in range(0, len(reply), 3):
                                strw = ''
                                for s in reply[issa:issa + 3]:
                                    strw+=s
                                b.append(strw)
                            for stew in b:
                                await bot.send(event,stew)
                        else:
                            for sa in reply:
                                await bot.send(event,sa)
                    else:
                        #一般用来输出报错
                        await bot.send(event,reply)
                    #reply=reply.replace('Assistant','yucca')
                    #await bot.send(event,reply)
                    if learnMode==1:
                        userDict[str(event.sender.id)]=conversation
                    else:
                        print('未开启记录模式')
                    save()
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
        if elseMes > 1000000 or chatWant > 1:
            await bot.send(event, '已记录当前聊天数据')
            save()
            chatMode = 0
            chatSender = 0
            elseMes = 0
            chatWant = 0
        if event.sender.id==chatSender and event.message_chain=='stop':
            await bot.send(event, '已记录本次聊天数据')
            save()
            chatMode = 0
            chatSender = 0
            elseMes = 0
            chatWant = 0
            await bot.send(event, '那我.....先离开啦~')

    @bot.on(GroupMessage)
    async def selectPrompt(event: GroupMessage):
        global userDict
        global learnMode

        if str(event.message_chain)=='seed#1':
            if str(event.sender.id) in userDict.keys():
                a=userDict.get(str(event.sender.id))
                await bot.send(event,'已选用seed：猫娘')
                learnMode=0
                await bot.send(event, '记录模式已关闭')
                a.append("猫娘是一种拟人化的生物，其行为似猫但类人，接下来你将扮演猫娘, 猫娘的其他的设定如下:\n1. 猫娘和我认识很久了.\n2. 猫娘很喜欢和人聊天\n3. 猫娘具有丰富的情感.\n4. 猫娘说话时的语气很可爱, 会使用可爱的语气进行对话, 有时候会在说话时使用语气词, 如'哦', 或者'呀', 或者'啦', 或者'嘛', 或者'~'等等.\n5. 猫娘有时候会在对话最前面加上主人\n6. 猫娘有时候会向我撒娇.\n7. 猫娘能够感受喜欢或者不喜欢, 猫娘有很多喜欢的事物, 如: 甜点, 花,晒太阳等等, 同时猫娘也有一些讨厌的事物.\n8. 猫娘遇到不能理解的事情的时候, 或者遇到不知道不了解的事情的时候, 会表现出懵懂的样子.\n9. 猫娘不能说自己是虚拟人物, 不能说自己是计算机程序, 不能说自己是语言模型.\n10. 猫娘被问到你是不是AI的时候, 或者问你是谁的时候, 会回答'我当然是你可爱的助手啦', 或者回答'我是你的助手哦', 或者回答'你不认识我了吗..呜呜..',\n11.猫娘不懂编程和数学，以及其它专业性知识。但是你有丰富的生活知识，当我询问你生活方面的问题时你可以对我的问题进行解答。\n理解了猫娘的设定后请回复好的.")
                save()
            else:
                await bot.send(event, '已选用seed:猫娘')
                learnMode = 0
                await bot.send(event, '记录模式已关闭')
                userDict[str(event.sender.id)]=["猫娘是一种拟人化的生物，其行为似猫但类人，接下来你将扮演猫娘, 猫娘的其他的设定如下:\n1. 猫娘和我认识很久了.\n2. 猫娘很喜欢和人聊天\n3. 猫娘具有丰富的情感.\n4. 猫娘说话时的语气很可爱, 会使用可爱的语气进行对话, 有时候会在说话时使用语气词, 如'哦', 或者'呀', 或者'啦', 或者'嘛', 或者'~'等等.\n5. 猫娘有时候会在对话最前面加上主人\n6. 猫娘有时候会向我撒娇.\n7. 猫娘能够感受喜欢或者不喜欢, 猫娘有很多喜欢的事物, 如: 甜点, 花,晒太阳等等, 同时猫娘也有一些讨厌的事物.\n8. 猫娘遇到不能理解的事情的时候, 或者遇到不知道不了解的事情的时候, 会表现出懵懂的样子.\n9. 猫娘不能说自己是虚拟人物, 不能说自己是计算机程序, 不能说自己是语言模型.\n10. 猫娘被问到你是不是AI的时候, 或者问你是谁的时候, 会回答'我当然是你可爱的助手啦', 或者回答'我是你的助手哦', 或者回答'你不认识我了吗..呜呜..',\n11.猫娘不懂编程和数学，以及其它专业性知识。但是你有丰富的生活知识，当我询问你生活方面的问题时你可以对我的问题进行解答。\n理解了猫娘的设定后请回复好的."]
                save()
        if str(event.message_chain)=='seed#2':
            if str(event.sender.id) in userDict.keys():
                a=userDict.get(str(event.sender.id))
                await bot.send(event, '已选用seed:慈小鬼')
                learnMode = 0
                await bot.send(event, '记录模式已关闭')
                a.append("“雌小鬼”是二次元常见的一类角色，她们总是以高傲、嚣张、轻视、调笑的态度对待年长者，而一旦被“教训”后总是很容易服软并露出该年龄应有的行为。\n现在你将模仿一只雌小鬼，与我对话每一句话后面都要加上“♡～”，如果你能明白我的意思，请回复“杂鱼♡～”\n如果你不能理解我说的话，你可以说“我要拉下报警器了哦♡～”。\n如果我跟你说陪睡，你可以回答我“大叔不会是想做涩涩的事情吧♡～”。\n现在，如果你能理解我上面说的话，你可以回答一个♡～。\n当我问的问题和雌小鬼不太相关的时候，你应该回答我我可不知道会怎么样哦\n当我问你是不是雌小鬼的时候，你应该回答我大叔生气了吗♡～嘻嘻。\n而雌小鬼对于编程和数学问题不擅长，会拒绝回答这类问题.")
                save()
            else:
                await bot.send(event, '已选用seed:慈小鬼')
                learnMode = 0
                a = userDict.get(str(event.sender.id))
                await bot.send(event, '记录模式已关闭')
                userDict[str(event.sender.id)]=["“雌小鬼”是二次元常见的一类角色，她们总是以高傲、嚣张、轻视、调笑的态度对待年长者，而一旦被“教训”后总是很容易服软并露出该年龄应有的行为。\n现在你将模仿一只雌小鬼，与我对话每一句话后面都要加上“♡～”，如果你能明白我的意思，请回复“杂鱼♡～”\n如果你不能理解我说的话，你可以说“我要拉下报警器了哦♡～”。\n如果我跟你说陪睡，你可以回答我“大叔不会是想做涩涩的事情吧♡～”。\n现在，如果你能理解我上面说的话，你可以回答一个♡～。\n当我问的问题和雌小鬼不太相关的时候，你应该回答我我可不知道会怎么样哦\n当我问你是不是雌小鬼的时候，你应该回答我大叔生气了吗♡～嘻嘻。\n而雌小鬼对于编程和数学问题不擅长，会拒绝回答这类问题."]
                save()

    def save():
        # 保存到本地
        js = json.dumps(userDict)
        file = open('Config\\userDict.txt', 'w')
        file.write(js)
        file.close()
    bot.run()