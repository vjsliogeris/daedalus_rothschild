import discord
from dotenv import load_dotenv
import os
import time
import subprocess
import asyncio

ID = 170838541855752192
dikt_ID = 516617064522317835
bals_ID = 786009733021696020
period = 30

class Daedalus(discord.Client):


    async def on_ready(self):
        self.current_song = None
        print('Logged on as {0}!'.format(self.user))
        diktatura = await self.fetch_guild(dikt_ID)
        morpheus = await diktatura.fetch_member(ID)
        kanalai = await diktatura.fetch_channels()
        balsas = None
        for kanalas in kanalai:
            if kanalas.id == bals_ID:
                balsas = kanalas
        VC = await balsas.connect()

        print("Connected to channel {0}".format(balsas))
        while True:
            command = "mpc current --host=/home/renamorcen/.config/mpd/socket"
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            filename = output[:-1]
            print(filename)
            if not self.current_song == filename:
                #Play song and change it
                self.current_song = filename
                VC.stop()
                VC.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename), 0.5))
            await asyncio.sleep(period)



load_dotenv()
token = os.getenv("DISCORD_TOKEN")

print("Starting bot...")
intents = discord.Intents().all()


botas = Daedalus(intents = intents)
botas.run(token)
print("Done!")
