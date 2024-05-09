"""Скрипт Setup.py для проекта по упаковке."""
from setuptools import setup

import os


def read_dependencies():
    """Получаем из requirements.txt зависимости по умолчанию."""
    filepath = os.path.join(os.path.dirname(__file__), 'cpu_checker', 'requirements.txt')
    with open(filepath) as requirements_file:
        dependencies = requirements_file.readlines()
        return [dependency for dependency in dependencies]


if __name__ == '__main__':
    setup(
        name='cpu_utilization_monitoring',
        version='0.1.3',
        author='Basov Ivan',
        author_email='demon_cuc@mail.ru',
        url='https://github.com/zeleniyToster/test_task_carbon_soft',
        download_url='https://github.com/zeleniyToster/test_task_carbon_soft/archive/refs/heads/master.zip',
        package_dir={'': 'cpu_checker'},
        package_data={
            '': ['*', 'requirements.txt', '*/requirements.txt'],
        },
        description='Тестовое задание для carbon soft.',
        python_requires='>=3.10.4',
        install_requires=[
              *read_dependencies(),
        ],
    )
