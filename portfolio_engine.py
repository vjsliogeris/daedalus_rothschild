"""portfolio_engine.py
"""

import pickle
import os
from random import randrange
import numpy as np
import random
import yfinance as yf
import time


INITIAL_CASH = 100000000

class player():
    def __init__(self, user_id):
        self.user_id = user_id
        self.cash = INITIAL_CASH
        self.stocks = {}
        self.shorts = []
        self.history = []

class history_entry():
    def __init__(self, ticker_str, quantity, price, when, nature):
        self.nature = nature
        self.ticker_str = ticker_str
        self.quantity = quantity
        self.price = price
        self.time = when

    def __str__(self):
        output = "{0}: ".format(time.strftime('%Y-%m-%d %H:%M:%S'), time.localtime(self.time))
        if self.nature == 0:
            output += "Bought       "
        if self.nature == 1:
            output += "Sold         "
        if self.nature == 2:
            output += "Opened short "
        if self.nature == 3:
            output += "Closed short "

        output += "{0} of {1} at {2} ({3})".format(
                self.quantity,
                self.ticker_str,
                self.price,
                self.price*self.quantity)
        return output

class short_position():
    def __init__(self, ticker_str: str,
            quantity: int, position_id: int,
            buy_price: float):
        self.ticker_str = ticker_str
        self.quantity = quantity
        self.buy_price = buy_price
        self.position_id = position_id


class portfolio_engine():
    def __init__(self, fname):
        """Load states of portfolios
        """
        self.fname = fname
        try:
            f = open(fname, "rb")
            self.players = pickle.load(f)
        except:
            f = open(fname, "wb")
            self.players = {}
            pickle.dump(self.players, f)
    def spawn_player(self, player_id):
        """Spawn a player instance
        """
        p = player(player_id)
        self.players[player_id] = p
        f = open(self.fname, "wb")
        pickle.dump(self.players, f)

    def reset(self, player_id: int) -> str:
        p = player(player_id)
        self.players[player_id] = p
        f = open(self.fname, "wb")
        pickle.dump(self.players, f)
        return "Reset complete"

    def buy(self, player_id: int, ticker_str: str, quantity: int) -> str:
        """Buy stonk
        """
        p = self.players[player_id]
        ticker = yf.Ticker(ticker_str)
        ticker_info = ticker.info
        price = ticker_info['regularMarketPrice']
        money_needed = price * quantity
        if money_needed > p.cash:
            return "Can't buy {0} worth of stock with {1} in the bank"\
                    .format(money_needed, p.cash)
        p.cash -= money_needed
        if ticker_str in p.stocks.keys():
            p.stocks[ticker_str] += quantity
        else:
            p.stocks[ticker_str] = quantity

        h_entry = history_entry(ticker_str, quantity, price, time.time(), 0)
        p.history.append(h_entry)
        
        self.players[player_id] = p
        f = open(self.fname, "wb")
        pickle.dump(self.players, f)

        return "Bought {0} of {1} stock at {2}".format(str(quantity), ticker_str, str(price))

    def sell(self, player_id: int, ticker_str: str, quantity: int) -> str:
        """sell stonk
        """
        p = self.players[player_id]
        ticker = yf.Ticker(ticker_str)
        ticker_info = ticker.info
        price = ticker_info['regularMarketPrice']
        if not ticker_str in p.stocks.keys():
            return "You do not have {0} in portfolio".format(ticker_str)
        stock_held = p.stocks[ticker_str]
        if stock_held < quantity:
            return "You have only {0} of {1} (Trying to sell {2}).".format(
                    stock_held,
                    ticker_str,
                    quantity)
        p.stocks[ticker_str] -= quantity
        p.cash += price * quantity

        h_entry = history_entry(ticker_str, quantity, price, time.time(), 1)
        p.history.append(h_entry)

        self.players[player_id] = p
        f = open(self.fname, "wb")
        pickle.dump(self.players, f)

        return "Sold {0} of {1} at {2}".format(quantity, ticker_str, price)

    def short_open(self, player_id: int, ticker_str: str, quantity: int) -> str:
        p = self.players[player_id]
        ticker = yf.Ticker(ticker_str)
        ticker_info = ticker.info
        price = ticker_info['regularMarketPrice']
        position_id = len(p.shorts)

        position = short_position(ticker_str, quantity, position_id, price)
        p.shorts.append(position)
        h_entry = history_entry(ticker_str, quantity, price, time.time(), 2)
        p.history.append(h_entry)

        self.players[player_id] = p
        f = open(self.fname, "wb")
        pickle.dump(self.players, f)
        return "Opened short position on {0} at {1} ({2})".format(ticker_str, price, quantity)

    def short_close(self, player_id: int, position_id: int):
        p = self.players[player_id]
        position = p.shorts.pop(position_id)
        quantity = position.quantity
        ticker_str = position.ticker_str
        ticker = yf.Ticker(ticker_str)
        ticker_info = ticker.info
        price = ticker_info['regularMarketPrice']
        price_gain = price - position.buy_price
        money_gain = price_gain * position.quantity
        p.cash += money_gain
        h_entry = history_entry(ticker_str, quantity, price, time.time(), 3)
        p.history.append(h_entry)

        self.players[player_id] = p
        f = open(self.fname, "wb")
        pickle.dump(self.players, f)
        return "Closed short position on {0} at {1}. Gained: {2}".format(ticker_str, price, money_gain)

    def shorts(self, player_id: int):
        p = self.players[player_id]
        shorts = p.shorts
        output = "ID|Ticker str|quantity|price\n"
        for short in shorts:
            output += f"{short.position_id}: {short.quantity} {short.ticker_str} at {short.buy_price}\n"
        return output

    def portfolio(self, player_id: int) -> str:
        outputstr = ""
        p = self.players[player_id]
        cash = p.cash
        outputstr += "Cash: {0}\n".format(cash)
        total_value = cash
        for ticker_str, quantity in p.stocks.items():
            print("Gathering {0}".format(ticker_str))
            ticker = yf.Ticker(ticker_str)
            ticker_info = ticker.info
            price = ticker_info['regularMarketPrice']
            outputstr += "{0}: {1} ({2}$)\n".format(ticker_str, quantity, price * quantity)
            total_value += price * quantity
        for position in p.shorts:
            ticker_str = position.ticker_str
            print("Gathering {0}".format(ticker_str))
            ticker = yf.Ticker(ticker_str)
            ticker_info = ticker.info
            price = ticker_info['regularMarketPrice']
            buy_price = position.buy_price
            money_diff = price - buy_price
            total_value += money_diff
            outputstr += "Open short {0}: {1} ({2}$)\n".format(ticker_str, quantity, money_diff)
    
        outputstr += "Total value: {0}\n".format(total_value)

        return outputstr

    def get_history(self, player_id: int) -> str:
        p = self.players[player_id]
        history = p.history
        output = ""
        for g in history:
            output += "{0}\n".format(g)
        return output

