# -*- coding: utf-8 -*-

from .goods import Goods
from .stock import Stock

class Logistic():
    def __init__(self, conn, farm):
        self.goods = Goods(conn=conn, farm=farm)
        self.stock = Stock(conn=conn, farm=farm)