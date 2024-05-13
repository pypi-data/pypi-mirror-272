# @copyright: 2024. All rights reserved.

from setuptools import setup

try:
    from pypandoc import convert_file
    long_description = convert_file('README.md', 'md')

except ImportError:
    long_description = """

    Log Better


    More information at: https://github.com/tactlabs/logplus.
"""

setup(name='logplus',
      description='Log Better',
      long_description=long_description,
      version='0.1.2',
      url='https://github.com/tactlabs/logplus',
      author='Raja CSP Raman',
      author_email='raja.csp@gmail.com',
      license='Apache2',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3'
      ],
      packages=['logplus'],
      install_requires=[
          'pypandoc>=1.4'
      ],
      entry_points={
          'console_scripts': [
              'encrypt=pinin.main:run'
          ]
      }
)