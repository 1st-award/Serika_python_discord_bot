import os
import discord
import logging
import army_date_calculate as army
import random
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json

TOKEN = os.environ["TOKEN"]

client = discord.Client()

class MyClient(discord.Client):
    async def on_ready(self):
        #건설로봇 준비완료
        print('{0}준비 완료!'.format(self.user))

    async def on_message(self, message):
        #DM에서 무슨 메세지를 보냈는데 log로 확인합니다.
        print("{0.author}에게서 온 DM : {0.content}".format(message))

    async def on_message(self, message):
        #메세지를 보낸 유저가 봇이 아닌 유저인지 확인해줍니다.
        if message.author.id == self.user.id:
            return
    
    # 인사를 건냅니다.
        if message.content.startswith('-안녕'):
            await message.reply('안녕하세요!!', mention_author=True)
    
    # 진짜 수정한거 맞는 지 확인합니다. 고쳐졌다면서 안고쳐져있지만        
        if message.content.startswith('-수정'):
            await message.reply('고쳐졌어요!!', mention_author=True)
    
    # 제작자의 남은 군생활을 알려줍니다.    
        if message.content.startswith('-복무일'):
            date = army.remain_days()
            date_percent = army.remain_days_percent()
            await message.channel.send("치비님의 남은 전역일 수는 " + date + "일이며 현재까지 " + date_percent + "%만큼 했습니다!")
    
    # 로또 번호를 뽑아줍니다. 낙첨되도 책임은 지지 않습니다...  
        if message.content.startswith('-로또'):
            # 로또 번호 1~45까지의 숫자를 뽑아줍니다.
            possible_number_list = random.sample(range(1,45), 6)
            # 로또 번호를 보기 편하게 숫자 크기 순으로 정렬해줍니다.
            possible_number_list = sorted(possible_number_list)
            # 로또 번호를 출력하기 위해 문자열로 바꾸고 출력하기 편하게 바꿔줍니다.
            number_list = ", ".join([str(numb) for numb in possible_number_list])
            await message.channel.send("이번 로또 추첨번호는 `" + number_list + "` 가 좋을 것 같아요!")
    
    # 0~10 중에서의 숫자를 뽑아줍니다. 
        if message.content.startswith('-추첨'):
            # 디스코드 이모지인 숫자들의 리스트
            possible_numb = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]
            # 숫자들의 리스트에서 하나를 뽑아줍니다.
            picked = random.choice(possible_numb)
            await message.channel.send("숫자 " + picked + "가 나왔어요!")
    
    # 선택장애를 위해 선택을 대신 해줍니다.
        if message.content.startswith('-선택'):
            # 메세지를 불러옵니다
            choice_msg = message.content
            # .split()을 위해 "-선택" 이라는 단어를 제거합니다.
            wanted_choice = choice_msg[3:]
            # 선택지를 나눠 리스트화시킵니다.
            select_choose = wanted_choice.split()
            # 리스트화 된 선택지에서 하나를 골라줍니다.
            choose = random.choice(select_choose)
            await message.channel.send(choose + "(이)가 좋을 것 같아요!")
        if message.content.startswith('-엑셀'):
            scope = ['https://spreadsheets.google.com/feeds']
            json_creds = os.getenv("GOOGLE_KEYS")
            creds_dict = json.loads(json_creds)
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
            credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_dict, scope)
            gc = gspread.authorize(credentials)
            gc1 = gc.open("리듬게임 스코어링 시트").worksheet('밀리시타')
            gc2 = gc1.get_all_values()
            japan_name = gc1.acell('B2').value
            korean_name = gc1.acell('C2').value
            difficulty = gc1.acell('E2').value
            perfect_note = gc1.acell('F2').value
            great_note = gc1.acell('G2').value
            good_note = gc1.acell('H2').value
            fastslow_note = gc1.acell('I2').value
            miss_note = gc1.acell('J2').value
            total_note = gc1.acell('K2').value
            max_combo = gc1.acell('L2').value
            full_combo = gc1.acell('M2').value
            best_score = str(gc1.acell('N2').value)
            await message.reply("> "+ japan_name +  "\n"
                                       "> " + korean_name +"\n"
                                       "> \n"
                                       ">   ** 누가 불렀누**                                          모치즈키 안나 (CV.난스)\n"
                                       "> \n"
                                       ">  **DIFFICULTY**      **PERFECT**       **GREAT**       **GOOD**       **FAST/SLOW**       **MISS**\n"
                                       ">           " + difficulty +"                      " + perfect_note +"                   "+ great_note +"                     "+ good_note +"                       "+ fastslow_note +"                       "+ miss_note +"\n"
                                       "> \n"
                                       "> **TOTAL NOTES**               **MAX COMBO**               **FULL COMBO**\n"
                                       ">           " + total_note +"                                   " + max_combo +"                          " + full_combo +"\n"
                                       "> \n"
                                       "> **TOTAL SCORE**                    " + best_score + "\n")
            try:
                scopes = ['https://spreadsheets.google.com/feeds']
                json_creds = os.getenv("GOOGLE_KEYS")
                token = json.dumps(str(json_creds))
                creds_dict = json.loads(token)
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
                creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
                
                gc = gspread.authorize(creds)
                gc1 = gc.open("리듬게임 스코어링 시트").worksheet('밀리시타')
                
                gc2 = gc1.get_all_values()
                japan_name = gc1.acell('B2').value
                korean_name = gc1.acell('C2').value
                difficulty = gc1.acell('E2').value
                perfect_note = gc1.acell('F2').value
                great_note = gc1.acell('G2').value
                good_note = gc1.acell('H2').value
                fastslow_note = gc1.acell('I2').value
                miss_note = gc1.acell('J2').value
                total_note = gc1.acell('K2').value
                max_combo = gc1.acell('L2').value
                full_combo = gc1.acell('M2').value
                best_score = str(gc1.acell('N2').value)
                await message.reply("> "+ japan_name +  "\n"
                                           "> " + korean_name +"\n"
                                           "> \n"
                                           ">   ** 누가 불렀누**                                          모치즈키 안나 (CV.난스)\n"
                                           "> \n"
                                           ">  **DIFFICULTY**      **PERFECT**       **GREAT**       **GOOD**       **FAST/SLOW**       **MISS**\n"
                                           ">           " + difficulty +"                      " + perfect_note +"                   "+ great_note +"                     "+ good_note +"                       "+ fastslow_note +"                       "+ miss_note +"\n"
                                           "> \n"
                                           "> **TOTAL NOTES**               **MAX COMBO**               **FULL COMBO**\n"
                                           ">           " + total_note +"                                   " + max_combo +"                          " + full_combo +"\n"
                                           "> \n"
                                           "> **TOTAL SCORE**                    " + best_score + "\n")
            except SyntaxError as err:
                await message.reply(err)
            except NameError as err1:
                await message.reply(err1)
            except KeyError as err2:
                await message.reply(err2)
            except AttributeError as err3:
                await message.reply(err3)
            except TypeError as err4:
                await message.reply(err4)
            except:
                await message.reply("에러 발생!")

     # 디스코드 내에서 사용할 수 있는 기능을 소개해줍니다.
        if message.content.startswith('-설명'):
            await message.channel.send("안녕하세요! 치비님의 인공비서 하코자키 세리카에요! \n\n현재 사용할 수 있는 기능으로는\n```fix\n-복무일 : 개발자의 남은 복무일수를 알려줍니다.\n"
                                       "-로또 : 로또 번호를 6개 선택해줍니다. 로또 번호를 추첨해서 뽑으면 뽑힐 때 기분이 더 좋아지는 효과가 있습니다.\n"
                                       "-추첨 : 랜덤된 숫자 0~10을 골라줍니다. 보통 누군가 한 명이 일을 몰빵 당할 때나 사용됩니다.\n"
                                       "-선택 [선택지1, 선택지2, ...] : 선택장애인 사람들을 위해 선택을 하게 해줍니다.```\n가 있어요!")
#기본적인 정보들을 로그에 출력해줍니다.
logging.basicConfig(level=logging.INFO)

client = MyClient()
client.run(TOKEN)
