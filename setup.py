from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='groundstation',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='UVic AERO',
      author_email='software@uvicaero.com',
      url='www.uvicaero.com',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'pillow',
          'tornado==5.1.1',
          'motor==2.0.0',
          'requests==2.20.0',
          'pymongo==3.7.2'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
