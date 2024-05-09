from pathlib import Path
from setuptools import setup

if __name__ == "__main__":
    this_directory = Path(__file__).parent
    long_description = (this_directory / "README.md").read_text()

    VERSION = '0.0.8'
    DESCRIPTION = 'Api para ver anime de AnimeFLV'
    PACKAGE_NAME = 'animeflvV2'
    AUTHOR = ''
    EMAIL = ''
    GITHUB_URL = ''

    setup(
        name = PACKAGE_NAME,
        packages = [PACKAGE_NAME],
        version = VERSION,
        license='MIT',
        description = DESCRIPTION,
        long_description_content_type="text/markdown",
        long_description=long_description,
        author = AUTHOR,
        author_email = EMAIL,
        url = GITHUB_URL,
        keywords = [],
        install_requires=[ 
            'requests',
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
        ],
    )