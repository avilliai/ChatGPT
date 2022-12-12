# ChatGPT-yirimirai

使用yirimirai调用chatgpt

需求：3.10>python>3.7

项目修改自[acheong08]的ChatGPT(https://github.com/acheong08/ChatGPT)

# 使用方法

  1.克隆此仓库
  
  2.运行pip install -r requirements.txt
  
  3.修改main.py中botqq,key,port与你mirai-api-http的保持一致
  
  4.如希望使用官方api，把你的apikey填入chatGPT.py中
  
  4.如希望连续聊天请获取token，并将其填入config.json。获取session_token可以参考[这里](https://lucent.blog/?p=99)
  
    此外你需要获取cf_clearance，和获取token的方法一样。
    
    最后是user_agent，[参考](https://blog.csdn.net/Inochigohan/article/details/120636769)
  
  4.运行main.py
  
# 指令如下

**这一部分是获取token后使用的**

  **开始聊天**
  
  *此命令用于开始会话*
  
  **stop**
  
  *终止会话，但保留本次聊天数据*
  
  **clear**
  
  *清除聊天数据(与当前用户的)*
 
 **使用官方api**
 
 /g
 
 /gt
  
  
  
# 如果你之前使用我分享的其他项目
  你可以将除main.py之外的的文件复制到项目中，复制main.py中的方法到bot.py中并导入对应的包
