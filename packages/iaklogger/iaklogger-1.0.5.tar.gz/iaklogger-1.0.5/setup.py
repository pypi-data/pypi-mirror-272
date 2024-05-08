
from distutils.core import setup
setup(
    name='iaklogger',         # How you named your package folder (MyLib)
    packages=['iaklogger'],   # Chose the same as "name"
    version='1.0.5',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Very basic and easy logger',
    long_description='Very basic and easy logger for python. It allows to print logs to the console and/or to a file. It also allows to mute logs by tags, mute all logs, show tags before the message, show time before the message, and set a maximum size for the log file.',
    author='Iakl',                   # Type in your name
    author_email='estebaniakl@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/Iakl/iaklogger',
    # I explain this later on
    download_url='https://github.com/Iakl/iaklogger/archive/refs/tags/v1.0.0.tar.gz',
    # Keywords that define your package best
    keywords=['logger', 'easy', 'print', 'log', 'basic', 'logging'],
    install_requires=[],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
