from setuptools import setup

with open("readme.md", "r") as arq:
    readme = arq.read()

setup(name='CustomTkinterMessagebox',
    version='0.0.1',
    license='MIT License',
    author='Jorge Magno',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='jorge.estudos0@gmail.com',
    keywords='customtkinter',
    description=u'Messagebox for CustomTkinter',
    packages=['CustomTkinterMessagebox'],
    install_requires=['pillow', 'customtkinter'],)