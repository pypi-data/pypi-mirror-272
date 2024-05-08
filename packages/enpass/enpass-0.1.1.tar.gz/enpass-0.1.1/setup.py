from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name = 'enpass',
    version = '0.1.1',
    description = 'Simple entropy password validator.',
    long_description= long_description,
    long_description_content_type = 'text/markdown',
    author = 'Andres Ordonez',
    packages=['enpass'],
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