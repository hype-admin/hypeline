from setuptools import setup

setup(
    name='hypeline',
    version='0.1',
    packages=['hypeline'],
    install_requires=[
        'gspread',
        'dropbox',
        'requests',
        'pandas',
        'ftrack_python_api',
        'tqdm'
    ],
)
