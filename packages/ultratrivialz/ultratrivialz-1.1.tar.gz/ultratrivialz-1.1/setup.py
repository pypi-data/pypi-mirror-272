from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setup(
    name = 'ultratrivialz',
    packages = ['ultratrivialz'],
    version = '1.1',
    license='MIT',
    description = 'ultratrivialz',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author = 'ochaaz',
    author_email = 'ocha@masrizky.com',
    url = 'https://github.com/ochaaz/ultratrivialz',
    download_url = 'https://github.com/ochaaz/ultratrivialz/archive/v_01.tar.gz',
    project_urls={
        'Documentation': 'https://github.com/ochaaz/ultratrivialz',
        'Funding': 'https://donate.pypi.org',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/ochaaz/ultratrivialz/',
        'Tracker': 'https://github.com/ochaaz/ultratrivialz/issues',
    },
    keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],
    install_requires=[
            'validators',
            'beautifulsoup4',
            'discordautochat',
            'discorudo',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
     dependencies= [
        'discordautochat',
        'discorudo'
    ]
)
