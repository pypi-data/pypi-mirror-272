from setuptools import setup


setup(name='CustomTkinterMessagebox',
    version='0.0.2',
    license='MIT License',
    author='Jorge Magno',
    long_description=open('readme.md').read(),
    long_description_content_type="text/markdown",
    author_email='jorge.estudos0@gmail.com',
    keywords='customtkinter',
    description=u'Messagebox for CustomTkinter',
    packages=['CustomTkinterMessagebox'],
    install_requires=['pillow', 'customtkinter'],)