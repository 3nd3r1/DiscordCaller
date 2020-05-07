import discord
import asyncio
import twilio.rest
from cryptography.fernet import Fernet
import mysql.connector
import app_config

#Database class -------------------------------->
class Database():
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    def connect(self):
        self.db = mysql.connector.connect(
            host = self.host,
            user = self.user,
            passwd = self.password,
            database = self.database
            )
        self.cursor = self.db.cursor()
    #Getting all numbers decrypted
    def GetAllNumbers(self):
        try:
            self.cursor.execute("SELECT * FROM numbers")
        except:
            self.connect()
            self.cursor.execute("SELECT * FROM numbers")
        numbers = [sec.fdecode(i[1]) for i in self.cursor.fetchall()]
        return numbers

    #Storing and crypting a number
    def StoreNumber(self, number):
        sql = "INSERT INTO numbers (number) VALUES (%s)"
        val = (sec.fencode(number),)
        #If timedout reconnect
        try:
            self.cursor.execute(sql, val)
        except:
            self.connect()
            self.cursor.execute(sql, val)
        self.db.commit()
        return True
    def DeleteNumber(self, number):
        sql = "DELETE FROM numbers WHERE number=%s"
        val = (sec.fencode(number),)
        try:
            self.cursor.execute(sql, val)
        except:
            self.connect()
            self.cursor.execute(sql, val)
        self.db.commit()
        return True
#Crypting class -------------------------->
class Secure():
    def __init__(self, key):
        self.f = Fernet(key)

    #Fernet encoding
    def fencode(self, password):
        encoded_pass = password.encode()
        return self.f.encrypt(encoded_pass).decode()

    #Fernet decrypt
    def fdecode(self, crypt):
        return self.f.decrypt(crypt.encode()).decode()

#Twilio app class ----------------------->
class TwilioApplication:
    def __init__(self, account_sid, auth_token):
        self.client = twilio.rest.Client(account_sid, auth_token)
    def callNumbers(self):
        print("[INFO] Calling all numbers..")
        for number in db.GetAllNumbers():
            call = self.client.calls.create(
                            machine_detection = 'DetectMessageEnd',
                            url=app_config.tw_xml,
                            to=number,
                            from_=app_config.tw_from_number
                        )

#Discord class ------------------------------------>
class DiscordApplication(discord.Client):
    async def on_ready(self):
        print("[INFO] Logged in as", self.user)

    async def on_message(self, message):
        #If message author is the bot thon do anything
        if message.author == self.user:
            return

        if "@everyone" in message.content and message.channel.id==app_config.dc_channel_id:
            #Call all the numbers
            print("[INFO] @everyone sent by",message.author)
            twclient.callNumbers()

        #Admin commands
        try:
            message.channel.guild
        except AttributeError:
            if message.author.id==app_config.dc_admin_id:
                #Add numbers EX: !addnumber 123123123,32132213
                #This is a bit sloppy but admin commands don't need much efficiency.
                if message.content.startswith("!addnumber"):
                    numbers = message.content.split(" ")[1].split(",")
                    storednumbers = db.GetAllNumbers()
                    added = 0
                    duplic = 0
                    for number in numbers:
                        if(number not in storednumbers):
                            db.StoreNumber(number)
                            added +=1
                        else:
                            duplic +=1
                    if(duplic==0):
                        await message.channel.send("Added all "+str(added)+" numbers")
                    else:
                        await message.channel.send("Added "+str(added)+" numbers, skipped "+str(duplic)+" duplicates")
                    print("[INFO]",message.author,"added numbers",str(numbers))
                
                #debug commands--------
                if message.content.startswith("!listnumbers") and app_config.debug==1:
                    numbers = db.GetAllNumbers()
                    await message.channel.send("All numbers: "+str(numbers))
                
                if message.content.startswith("!delnumber") and app_config.debug==1:
                    numbers = message.content.split(" ")[1].split(",")
                    storednumbers = db.GetAllNumbers()
                    deleted = 0
                    for number in numbers:
                        if number in storednumbers:
                            db.DeleteNumber(number)
                            deleted +=1
                    await message.channel.send("Deleted: "+str(deleted)+" numbers")
if __name__ == "__main__":
    sec = Secure(app_config.f_secret_key)
    db = Database(app_config.db_host, app_config.db_user, app_config.db_pass, app_config.db_name)

    twclient = TwilioApplication(app_config.tw_account_sid, app_config.tw_auth_token)
    dcclient = DiscordApplication()
    dcclient.run(app_config.dc_token)