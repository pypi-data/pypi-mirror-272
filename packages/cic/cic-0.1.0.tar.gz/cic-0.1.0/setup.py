from setuptools import setup, find_packages

setup(
    name='cic',
    version='0.1.0',
    author='Eren Güven',
    author_email='erenguven0@gmail.com',
    description='A build and deployment webapp',
    # long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/CIC/',
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.7',
)
