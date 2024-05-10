from setuptools import setup, find_packages

setup(
    name='first_glance',
    version='1.0.1',
    author='Jordan Kanius',
    author_email='Kaniusjordan@gmail.com',
    description='Quick plotting and examination for early analysis of data',
    long_description='Python package used for early inital analysis with the ability to return plots(boxplots, histograms and heatmap)\
    and a count of nulls, datatype, and descriptive stats for each column within the data',
    long_description_content_type='text/markdown',
    url='https://github.com/Kanustu/analysis_reporting',
    packages=find_packages(),
    install_requires=['pandas', 'seaborn'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
