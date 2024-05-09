from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='bradescoPixCTS',
    version='0.1',
    license='MIT License',
    url='https://pypi.org/user/monetizze/',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Monetizze',
    author_email='payments@monetizze.com.br',
    keywords='bradesco',
    description=u'SDK Bradesco PIX V8',
    packages=find_packages(),)
