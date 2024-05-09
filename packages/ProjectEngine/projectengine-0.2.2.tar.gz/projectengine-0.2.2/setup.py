from setuptools import setup 
  
setup( 
    name='ProjectEngine', 
    version='0.2.2', 
    description='Basic PyOpenGl project', 
    author='Oliver Wilkinson', 
    author_email='otwilkinsonuk@icloud.com', 
    packages=['ProjectEngine'], 
    install_requires=[ 
        'pygame', 
        'PyOpenGl',
        'objloader'
    ],
    long_description="see https://projectengine.vercel.app/ for decumentation" 
) 
