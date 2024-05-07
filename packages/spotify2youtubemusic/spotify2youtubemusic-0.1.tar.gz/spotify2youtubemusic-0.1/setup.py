from setuptools import setup
from setuptools.command.install import install
from spotify2youtubemusic import download


class CustomInstall(install):
    def run(self):
        download.download_file()
        super().run()


setup(
    name='spotify2youtubemusic',
    version='0.1',
    packages=['spotify2youtubemusic'],
    install_requires=[
        'requests',
    ],
    cmdclass={
        'install': CustomInstall,
    },
    zip_safe=False
)
