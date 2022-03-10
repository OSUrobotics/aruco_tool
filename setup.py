from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='aruco_tool',
    version='0.3.2',    
    description='Aruco Code pose detection library for use in my lab projects.',
    url='https://github.com/NotCras/aruco_tool/',
    download_url='https://github.com/NotCras/aruco_tool/archive/refs/tags/v0.3.2.tar.gz',
    author='John Morrow',
    author_email='morrowjo@oregonstate.edu',
    license='MIT',
    packages=['aruco_tool'],
    keywords=['aruco', 'image'], 
    install_requires=['pandas',
                      'numpy',
                      'opencv-contrib-python',
                      'matplotlib'                    
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
