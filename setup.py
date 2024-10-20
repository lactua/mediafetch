from setuptools import setup

setup(
   name='mediafetch',
   version='1.1',
   description='A media fetcher',
   author='lactua',
   author_email='rei.lactua.dsc@gmail.com',
   packages=['mediafetch'],  #same as name
   install_requires=['requests', 'pillow'], #external packages as dependencies
)