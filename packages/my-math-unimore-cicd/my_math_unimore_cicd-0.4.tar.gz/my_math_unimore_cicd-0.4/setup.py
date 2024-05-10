from setuptools import setup 
  
setup( 
    name='my_math_unimore_cicd', 
    version='0.4', 
    description='A sample Python package to test CI/CD', 
    long_description='A sample Python package to test CI/CD',
    author='Angelo Ferrando', 
    author_email='angelo.ferrando42@gmail.com', 
    packages=['my_math', 'pippo', ''], 
    install_requires=['pytest'], 
) 