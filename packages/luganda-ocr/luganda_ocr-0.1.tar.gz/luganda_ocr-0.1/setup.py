from setuptools import setup, find_packages

setup(
    name='luganda_ocr',
    version='0.1',
    author='Beijuka Bruno',
    author_email='lugandaocr@gmail.com',
    description='An OCR package for Luganda language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_data={'luganda_ocr': ['sentenceModel.h5']},
    install_requires=[
        'tensorflow>=2.14.0,<3.0.0',  
        'numpy',
        'pandas',
    ],
)

