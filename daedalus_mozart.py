import discord
from dotenv import load_dotenv
import os
import time
import subprocess
import asyncio

import playlist_engine

#prefix gal koki "#!"

ID = 170838541855752192
dikt_ID = 516617064522317835
bals_ID = 786009733021696020
period = 1

class Daedalus(discord.Client):

    async def on_ready(self):
        self.prefix = "#!"
        self.playlist_engine = playlist_engine.playlist_engine()

        print('Logged on as {0}!'.format(self.user))
        diktatura = self.get_guild(dikt_ID)
        morpheus = diktatura.get_member(ID)
        kanalai = await diktatura.fetch_channels()
        balsas = diktatura.get_channel(bals_ID)
        self.VC = await balsas.connect()
        self.chan = balsas
        print("Connected to channel {0}".format(balsas))
        await self.life_loop()

    async def reconnect(self):
        print('Logged on as {0}!'.format(self.user))
        diktatura = self.get_guild(dikt_ID)
        morpheus = diktatura.get_member(ID)
        kanalai = await diktatura.fetch_channels()
        balsas = diktatura.get_channel(bals_ID)
        self.VC = await balsas.connect()
        self.chan = balsas
        print("Connected to channel {0}".format(balsas))
        await self.life_loop()

    async def on_message(self, message):
        """Handle interaction of users with bot.
        """
        content = message.content
        author = message.author
        text_channel = message.channel
        if content[:2] == self.prefix:
            splits = content.split(" ")

            operation = splits[0]
            operands = splits[1:]
            operand = ""
            for op in operands:     #Cancer
                operand += op
                operand += " "

            operation = operation[2:]
            if operation == "p":
                #await text_channel.send("Trying to play {0}".format(operands))
                response = self.playlist_engine.download_song(operand)
                await text_channel.send(response)
            elif operation == "q":
                if len(operand) == 0:
                    n = 10
                else:
                    n = int(operand)
                response = self.playlist_engine.get_playlist(n)
                await text_channel.send(response)
            elif operation == "shuffle":
                await text_channel.send("Shuffling..")
                self.playlist_engine.shuffle()
            elif operation == "skip":
                if not len(operand) == 0:
                    n = int(operand)
                    self.playlist_engine.skip(n)
                self.VC.stop()
            elif operation == "help":
                helptext = open("helptext.txt","r").read()
                await text_channel.send(helptext)
            elif operation == "force_connect":
                await self.reconnect()
            else:
                await text_channel.send("\"{0}\": Not implemented".format(operation))

#        else:
#            pass abuse

    async def life_loop(self):
        while True:
            if not self.VC.is_connected():
                await asyncio.sleep(period)
                await self.reconnect()
            if not self.VC.is_playing():
                filename = self.playlist_engine.sample()
#                filename = 'assets/Born In Da Hood.mp4'
                print("Playing {0}".format(filename))
                self.VC.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename), 0.25))
            await asyncio.sleep(period)



load_dotenv()
token = os.getenv("DISCORD_TOKEN")

print("Starting bot...")
intents = discord.Intents.all()
intents.members = True

botas = Daedalus(intents = intents)
botas.run(token)
print("Done!")
