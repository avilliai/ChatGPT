# -*- coding: utf-8 -*-
from mirai import Mirai, FriendMessage, WebSocketAdapter,GroupMessage

from chatGPT import GPT


def main(bot):
    @bot.on(GroupMessage)
    async def gptGene(event: GroupMessage):
        if str(event.message_chain).startswith('/'):
            a = str(event.message_chain)[0:]
            print('即将发送' + a)
            backst = GPT(a)
            print('已返回')
            if len(backst) > 500:
                asf = cut(backst, 500)
                for i in asf:
                    await bot.send(event, i)
            else:
                await bot.send(event, backst)
    def cut(obj, sec):
        return [obj[i:i + sec] for i in range(0, len(obj), sec)]