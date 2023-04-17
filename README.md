# ChatGPT-yirimirai

使用yirimirai+revChatGpt调用chatgpt

需求：3.10>python>3.7

需要先安装[mirai-api-http](https://github.com/project-mirai/mirai-api-http)

项目修改自[acheong08的revChatGPT](https://github.com/acheong08/ChatGPT)

# 使用方法

  1.克隆此仓库
  
  2.打开cmd运行pip install -r requirements.txt
  
  3.修改main.py中botqq,key,port与你mirai-api-http的保持一致
  
  4.如希望使用官方api，把你的apikey填入chatGPT.py中
  
  4.1如希望使用revChatGPT请获取token，并将其填入config.json。获取session_token可以参考[这里](https://lucent.blog/?p=99)
  
  4.2此外你需要获取cf_clearance，和获取token的方法一样。![image](https://user-images.githubusercontent.com/99066610/206945384-3d42acd2-7bc0-46b5-8d72-01085464ad06.png)

    
  4.3最后是user_agent，[参考](https://blog.csdn.net/Inochigohan/article/details/120636769)
  
  4.4.打开cmd运行pip install cf_clearance2-0.28.3.tar.gz
  
  5.运行main.py
  
# 指令如下

**这一部分是获取token后使用的**

  **开始聊天前可指定seed**
  
  seed#1
  
  seed#2

  **开始聊天/chat**
  
  *此命令用于开始会话,使用revChatGPT是 开始聊天 官方api则是 chat*
  
  **stop**
  
  *终止会话，但保留本次聊天数据*
  
  **clear**
  
  *清除聊天数据(与当前用户的)*
 
 **使用官方api**
 
 /g
 
 /gt
  
 chat
  
  
# 如果你之前使用我分享的其他项目
  你可以将除main.py之外的的文件复制到项目中，复制main.py中的方法到bot.py中并导入对应的包
