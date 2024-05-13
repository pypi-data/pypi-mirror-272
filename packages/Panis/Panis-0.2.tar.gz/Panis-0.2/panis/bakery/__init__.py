# -*- coding: utf-8 -*-

from .dough import Dough
from .recipe import Recipe
from .product import Product
from .shape import Shape
from .batch import Batch
from .process import Process
from .allocation import Allocation
from .parameter import Parameter

class Bakery():
    def __init__(self, conn, farm):
        self.dough = Dough(conn=conn, farm=farm)
        self.recipe = Recipe(conn=conn, farm=farm)
        self.product = Product(conn=conn, farm=farm)
        self.shape = Shape(conn=conn, farm=farm)
        self.batch = Batch(conn=conn, farm=farm)
        self.process = Process(conn=conn, farm=farm)
        self.allocation = Allocation(conn=conn, farm=farm)
        self.parameter = Parameter(conn=conn, farm=farm)
