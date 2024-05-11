from setuptools import setup, find_packages

setup(
    name='AxleSpacing',
    version='0.1',
    packages=find_packages(),
    description='A Python library for vehicle axle spacing detection.',
    author='Vefa A.',
    author_email='vefa@connectedwise.com',
    url='https://github.com/connected-wise/BWIM_ComputerVision/tree/main/AxleSpacing',
    install_requires=[
        'opencv-python-headless',  # Assuming you are using OpenCV
        'numpy',
        'pandas',
        'torch',
        'matplotlib',
        'Pillow',  # PIL is part of Pillow
        'tqdm',
        'ultralytics',  # Make sure this is the correct package name on PyPI
        'supervision'  # Make sure this is the correct package name on PyPI
    ],
)