from setuptools import setup, find_packages

setup(
    name='tse_motion',
    version='0.1.7',
    packages=find_packages(),
    install_requires=[
        'torch',
        'monai',
        'nibabel',
        'torchvision'
    ],
    include_package_data=True,
    package_data={
        'tse_motion': ['checkpoint/weight_20.pth'],
    },
    entry_points={
        'console_scripts': [
            'rate-artifact=tse_rating.artifact_rating:main',
        ],
    },
    author='Jinghang Li',
    author_email='jinghang.li@pitt.edu',
    description='A package to rate motion artifacts in medical images.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jinghangli98/tse-rating',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
