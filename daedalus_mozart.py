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
        self.current_song = None
        self.prefix = "#!"
        self.playlist_engine = playlist_engine.playlist_engine()
        self.skippers = 0

        print('Logged on as {0}!'.format(self.user))
        diktatura = self.get_guild(dikt_ID)
        morpheus = diktatura.get_member(ID)
        kanalai = await diktatura.fetch_channels()
        balsas = diktatura.get_channel(bals_ID)
        self.VC = await balsas.connect()
        self.chan = balsas
        present_members = self.chan.members
        self.playlist_engine.connect_lads(present_members)
        print("Connected to channel {0}".format(balsas))
        await self.life_loop()


    async def on_message(self, message):
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
            if type(message.channel) != discord.DMChannel:
                await message.delete()
            if operation == "p":
                #await text_channel.send("Trying to play {0}".format(operands))
                print("Trying to play {0}".format(operand))
                response = self.playlist_engine.download_song(operand, author)
                await author.send(response)
            elif operation == "q":
                response = self.playlist_engine.get_playlist_author(author)
                await author.send(response)
            elif operation == "d":
                response = self.playlist_engine.delete(author, int(operand))
                await author.send(response)
            elif operation == "s":
                self.skippers += 1
                n_nariai = len(self.chan.members)-1
                if self.skippers*2 > n_nariai: #Pakankamai balsavo
                    await text_channel.send("Skippinam...")
                    self.VC.stop()
                else: #Nepakankamai balsavo
                    response = "{0} zmoniu nori skippinti. Skippui reikia bent puse esanciu zmoniu.".format(self.skippers)
                    await text_channel.send(response)
            else:
                await text_channel.send("Nesupratau ka reiskia \"{0}\"".format(operation))
#        else:
#            pass abuse

    async def life_loop(self):
        while True:
            present_members = self.chan.members
            self.playlist_engine.connect_lads(present_members)
            if not self.VC.is_playing():
                filename = self.playlist_engine.sample()
                print("Playing {0}".format(filename))
                self.VC.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename), 0.5))
            await asyncio.sleep(period)



load_dotenv()
token = os.getenv("DISCORD_TOKEN")

print("Starting bot...")
intents = discord.Intents.all()
intents.members = True

botas = Daedalus(intents = intents)
botas.run(token)
print("Done!")
