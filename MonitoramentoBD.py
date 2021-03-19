#-*- coding: utf-8 -*-
from telethon import TelegramClient, events, sync
from datetime import datetime, timedelta
from telethon.tl.types import UpdateShortMessage
import time, threading
import telnetlib
import pymssql
# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

user_atual = 'roboMonitoramentoDB'
api_id = SUBSTITUIR PELO ID DO ROBÔ DO TELEGRAM
api_hash = 'SUBSTITUIR PELO HASH DO ROBÔ DO TELEGRAM'
global client
client = TelegramClient(user_atual, api_id, api_hash)
client.start(bot_token='SUBSTITUIR PELO TOKEN DO ROBÔ DO TELEGRAM')
print("Detalhes do Robo:\n")
print(client.get_me().stringify())
global top5_ant
global top5
top5_ant = [1,2,3,4,5]
top5 = [1,2,3,4,5]
chat_id = SUBSTITUIR PELO ID DO CHAT DO TELEGRAM ONDE SERÁ DISPARADO O ALERTA


con = pymssql.connect(host = 'SUBSTITUIR PELO IP:PORTA DO SERVIDOR DO BANCO DE DADOS',user = 'SUBSTITUIR PELO USUARIO DO BANCO DE DADOS',password = 'SUBSTITUIR PELA SENHA DO BANCO DE DADOS',database = 'SUBSTITUIR PELO NOME DO BANCO DE DADOS')


@client.on(events.NewMessage)
async def my_event_handler(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    user = sender.username
    print(str(chat))
    t_now = datetime.now()
    
    if event.raw_text.find("Status Monitoramento DB")!=-1 or event.raw_text.find("Status monitoramento db")!=-1 or event.raw_text.find("status monitoramento db")!=-1:
        await client.send_message(entity=chat, message="Monitoramento OK")
    else:
        await client.send_message(entity=chat, message="Digite uma das opcoes: Status monitoramento db")
	
	

async def sendMessage(ent,msg):
    global client
    print(ent)
    print(msg)
    await client.send_message(entity=ent, message=msg)

def checarMonitoramentoDB():
    global top5_ant
    global top5
    cursor = con.cursor()
    # SUBSTITUIR CONSULTAS ABAIXO PELA COLUNA DA TABELA COM INFORMACAO DA DATA, ID E MENSAGEM DO ALERTA
    cursor.execute('select top 5 dt_alert from alert order by dt_alert desc')
    datas = cursor.fetchall()
    cursor.execute('select top 5 id_alert from alert order by id_alert desc')
    top5 = cursor.fetchall()
    cursor.execute('select top 5 Ds_Message from alert order by id_alert desc')
    msgs = cursor.fetchall()
    for i in range(0,len(top5)):
        tem=0
        for alert_anterior in top5_ant:
            if top5[i]==alert_anterior:
                tem=1
        if tem==0:
            client.loop.create_task(sendMessage(ent=chat_id, msg=str(msgs[i])+" - "+str(datas[i][0])))
    top5_ant = top5;

    threading.Timer(1, checarMonitoramentoDB).start()  


checarMonitoramentoDB()
while (1==1):
    HoraAtual = datetime.now()
    client.run_until_disconnected()   
    
