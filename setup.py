from setuptools import setup, find_packages

setup(
    name='hypeline',
    version='0.1',
    py_modules=find_packages(where='.'),
    install_requires=[
        'gspread',
        'dropbox',
        'requests',
        'pandas',
        'ftrack_python_api',
        'tqdm'
    ],
)
