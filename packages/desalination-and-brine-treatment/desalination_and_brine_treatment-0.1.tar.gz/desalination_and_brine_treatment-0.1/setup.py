#setup.py

from setuptools import setup, find_packages

setup(
      name='desalination_and_brine_treatment',
      version='0.1',
      description='A simulation tool for desalination and brine treatment technologies',
      packages=find_packages(),
      url="https://github.com/rodoulak/Desalination-and-Brine-Treatment-Simulation-",
      author="rodoulak",
      author_email="r.ktori@tudelft.nl",
      license="MIT",
      install_requires=[
          "numpy>=1.0",
          "pandas>=1.0",  # Include pandas as a dependency
        ],
      )