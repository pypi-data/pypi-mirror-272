from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='vecfield',
  version='1.0.0',
  author='SorbetKipit',
  author_email='ibk07@yandex.ru',
  description='Module for working with vector and scalar fields',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/SorbetKipit/jubilant-barnacle/tree/main',
  packages=find_packages(),
  install_requires=['requests>=2.25.1','sympy>=1.12','matplotlib>=3.8.4','numpy>=1.26.4'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='python vectorifeld scalarfield',
  project_urls={
    'Documentation': 'https://github.com/SorbetKipit/jubilant-barnacle/blob/main/README.md'
  },
  python_requires='>=3.11'
)