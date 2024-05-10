from setuptools import setup, find_packages

setup(
    name='AI_classifier',
    version='1.0',
    author='Nithin sai Adupa',
    author_email='nithinsaiadupa@gmail.com',
    description='A package for text classification using transformers models which classifies text whether it is AI generated or human written',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/saiadupa/AI_classifier',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
