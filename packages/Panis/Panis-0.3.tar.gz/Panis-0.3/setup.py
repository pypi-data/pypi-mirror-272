# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
   name='Panis',
   version='0.3',
   description='Commandes et pesées de boulangerie au levain',
   author='Frémi',
   author_email='fremi@protonmail.com',
   packages=find_packages(),
   install_requires=['numpy',
                     'pandas',
                     'tksheet',
                     'ttkthemes'], #external packages as dependencies
#   package_data={
#        '': ['*.tcl', '*.png'],
#    },
)
