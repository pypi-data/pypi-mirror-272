# -*- coding: utf-8 -*-

from .delivery import Delivery
from .client import Client
from .distribution import Distribution
from .order import Order
from .product import Product

class Sales():
    def __init__(self, conn, farm):
        self.delivery = Delivery(conn=conn, farm=farm)
        self.client = Client(conn=conn, farm=farm)
        self.distribution = Distribution(conn=conn, farm=farm)
        self.order = Order(conn=conn, farm=farm)
        self.product = Product(conn=conn, farm=farm)