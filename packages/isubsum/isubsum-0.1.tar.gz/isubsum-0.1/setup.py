from setuptools import setup

setup(
    name='isubsum',
    version='0.1',
    py_modules=['isubsum'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        isubsum=isubsum:main
    ''',
)

