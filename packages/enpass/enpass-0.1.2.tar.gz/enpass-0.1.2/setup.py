from setuptools import setup, find_packages

with open('README.md') as file:
    long_description = file.read()

setup(
    name = 'enpass',
    version = '0.1.2',
    description = 'Simple entropy password validator.',
    long_description= long_description,
    long_description_content_type = 'text/markdown',
    author = 'Andres Ordonez',
    packages=find_packages(),
    url='https://github.com/Aresshu/enpass',
    license = 'MIT',
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python",
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords = "entropy password validator strength",
)