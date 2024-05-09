from setuptools import setup

setup(
    name='picdiffbox',
    version='1.0.0',
    packages=['picdiffbox'],
    install_requires=[
        'opencv-python',
        'scikit-image',
        'numpy',
    ],
    author='Tushar Arora',
    author_email='Tushar.aka.datascientist@gmail.com',
    description='A Python library to compare two images and draw bounding boxes around the differences.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TUSHAR-PERSPECTIVE/picdiffbox',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
