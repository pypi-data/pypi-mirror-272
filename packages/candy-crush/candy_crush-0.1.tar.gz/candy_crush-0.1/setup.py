from setuptools import setup, find_packages

setup(
    name='candy_crush',  
    version='0.1',
    author='Alex',
    author_email='zuxell447@gmail.com',
    packages=find_packages(),
    install_requires=[  
        'numpy',  
        'requests'
    ],
    license='GPL (General Public License)', 
    description='candy crush optimal utility bot', 
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown', 
)
