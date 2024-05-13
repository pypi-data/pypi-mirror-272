from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='pyrepka',
    version='1.0.1',
    author='oshkov',
    author_email='sasha.oshkov03@gmail.com',
    description='Модуль для работы с реферальной программой "Репка"',
    long_description=readme(),
    long_description_content_type='text/markdown; text/html',
    url='https://github.com/oshkov/py-repka',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='Реферальная программа',
    project_urls={
        'GitHub': 'https://github.com/oshkov'
    },
    python_requires='>=3.6'
)