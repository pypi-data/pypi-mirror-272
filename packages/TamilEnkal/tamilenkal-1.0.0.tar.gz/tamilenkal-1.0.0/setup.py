from setuptools import setup, find_packages

setup(
    name='TamilEnkal',
    version='1.0.0',
    packages=find_packages(),
    author='Kathir Karky',
    author_email='kathirkarky@gmail.com',
    description='A package for Tamil numeral operations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kathirkarky/TamilEnkal/',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)
