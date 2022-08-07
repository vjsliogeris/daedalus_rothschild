import asyncio
import os
import subprocess
import time

from dotenv import load_dotenv
import discord

from portfolio_engine import portfolio_engine

#prefix gal koki "#!"

ID = 170838541855752192
dikt_ID = 516617064522317835
bals_ID = 786009733021696020
period = 1

class Daedalus(discord.Client):

    async def on_ready(self):
        self.prefix = "#!"
        print('Logged on as {0}!'.format(self.user))
        diktatura = self.get_guild(dikt_ID)
        morpheus = diktatura.get_member(ID)
        kanalai = await diktatura.fetch_channels()
        self.portfolios = portfolio_engine("portfolios.pickle")
        print("on")

    async def reconnect(self):
        print('Logged on as {0}!'.format(self.user))
        diktatura = self.get_guild(dikt_ID)
        morpheus = diktatura.get_member(ID)
        kanalai = await diktatura.fetch_channels()
        self.portfolios = portfolio_engine("portfolios.pickle")

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
            if operation == "start":
                self.portfolios.spawn_player(author.id)
                await text_channel.send("Player spawned")
            elif operation == "buy":
                ticker = operands[0]
                quantity = int(operands[1])
                response = self.portfolios.buy(author.id, ticker, quantity)
                await text_channel.send(response)
            elif operation == "sell":
                ticker = operands[0]
                quantity = int(operands[1])
                response = self.portfolios.sell(author.id, ticker, quantity)
                await text_channel.send(response)
            elif operation == "open_short":
                ticker = operands[0]
                quantity = int(operands[1])
                response = self.portfolios.short_open(author.id, ticker, quantity)
                await text_channel.send(response)
            elif operation == "close_short":
                position_id = int(operands[0])
                response = self.portfolios.short_close(author.id, position_id)
                await text_channel.send(response)
            elif operation == "shorts":
                response = self.portfolios.shorts(author.id)
                await text_channel.send(response)
            elif operation == "portfolio":
                response = self.portfolios.portfolio(author.id)
                await text_channel.send(response)
            elif operation == "history":
                response = self.portfolios.get_history(author.id)
                await text_channel.send(response)
            elif operation == "reset":
                response = self.portfolios.reset(author.id)
                await text_channel.send(response)
            elif operation == "help":
                await text_channel.send(helptext)
            else:
                await text_channel.send("\"{0}\": Not implemented".format(operation))


load_dotenv()
token = os.getenv("DISCORD_TOKEN")
print(token)

print("Starting bot...")
intents = discord.Intents.all()
intents.members = True

botas = Daedalus(intents = intents)
botas.run(token)
print("Done!")
