from setuptools import setup

setup(
    name='xdcc-grabber',
    version='0.1.0',
    packages=['xdcc_grabber'],
    entry_points={
        'console_scripts': [
            'xdcc-grabber = xdcc_grabber.__main__:main']},
    install_requires=[
        'irc3>=1.1.7',
        'fastapi>=0.70.1',
        'uvicorn>=0.16.0',
        'websockets>=10.1',
    ])
