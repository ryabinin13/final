# userservice/setup.py
from setuptools import setup, find_packages

setup(
    name='userservice',
    version='0.1.0',
    packages=find_packages(),  # Автоматически находит все пакеты в директории
    # Или, если нужно более явно: packages=['userservice'],
    install_requires=[
        # Здесь можно указать зависимости, специфичные для userservice
    ],
)
