from setuptools import setup

setup(
    name='hypeline',
    version='0.1',
    py_modules=[
        'hypeline.hypeline',
        'hypeline.hypeline.files_tools',
        'hypeline.hypeline.maya_ascii',
        'hypeline.hypeline.maya_prompt'
        ],
    install_requires=[
        'gspread',
        'dropbox',
        'requests',
        'pandas',
        'ftrack_python_api',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [],
        'gui_scripts': [],
        'hypeline': ['hypeline = hypeline.hypeline']
    },
)
