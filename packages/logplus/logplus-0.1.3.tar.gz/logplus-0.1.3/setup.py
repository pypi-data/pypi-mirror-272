# @copyright: 2024. All rights reserved.

from setuptools import setup, find_packages

with open("README.rst", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst", encoding="utf-8") as history_file:
    history = history_file.read()

requirements = [requirement for requirement in open('requirements.txt', encoding="utf-8")]

setup(
    name='logplus',
    description='Log Better',
    long_description= readme + "\n\n" + history ,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    version='0.1.3',
    url='https://github.com/tactlabs/logplus',
    author='Raja CSP Raman',
    author_email="info@tactii.com",
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(include=["logplus", "logplus.*"]),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'logplus=logplus.cli:main'
        ]
    },
    python_requires=">=3.7",
    keywords="logplus",
    zip_safe=False
)