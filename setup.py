from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

install_reqs = parse_requirements('requirements.txt', session='hack')

setup(
    name='trustBraker',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'click==8.1.3',
        'python-dotenv==1.0.0',
        'requests==2.28.2',
        'simple_term_menu',
    ],
    entry_points='''
    [console_scripts]
    trustBreaker=trustBreaker:trustBreaker
    '''
)
