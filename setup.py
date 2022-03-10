from setuptools import setup

setup(
    name='aruco_tool',
    version='0.3.1',    
    description='Aruco Code pose detection library for use in my lab projects.',
    url='https://github.com/NotCras/aruco_tool/',
    download_url='https://github.com/NotCras/aruco_tool/archive/refs/tags/v0.3.0.tar.gz',
    author='John Morrow',
    author_email='morrowjo@oregonstate.edu',
    license='MIT',
    packages=['aruco_tool'],
    keywords=['aruco', 'image'], 
    install_requires=['pandas',
                      'numpy',
                      'opencv-contrib-python'                    
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.9',
    ],
)
