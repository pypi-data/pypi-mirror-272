from setuptools import setup, find_packages

setup(
    name='ExcelExtractorJsonPDF',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'reportlab'
    ],
    author='Ivan APEDO',
    author_email='apedoivan@gmail.com',
    description='Python package for converting data from Excel to JSON and PDF',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/IvanGael/ExcelExtractorJsonPDF',
    license='MIT',
)
