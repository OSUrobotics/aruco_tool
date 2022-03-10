from setuptools import setup

setup(
    name='aruco_tool',
    version='0.2.0',    
    description='Aruco Code pose detection library for use in my lab projects.',
    url='https://github.com/NotCras/aruco_tool',
    author='John Morrow',
    author_email='morrowjo@oregonstate.edu',
    license='MIT',
    packages=['aruco_tool'],
    install_requires=['pandas',
                      'numpy',
                      'opencv-contrib-python'                    
                      ],

    classifiers=[
        'Development Status :: 4 - Beta', 
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.9',
    ],
)
