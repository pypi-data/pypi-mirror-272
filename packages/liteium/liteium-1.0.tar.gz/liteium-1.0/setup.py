from setuptools import setup, find_packages


setup(
    name='liteium',
    version='1.0',
    description='Description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='El Bettioui Reda',
    author_email='redaelbettioui@gmail.com',
    url='https://github.com/XredaX/liteium',
    packages=find_packages(),
    install_requires=[
        'selenium==4.19.0',
        'urllib3==1.26.16',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
