from setuptools import setup, find_packages
try:
    from install_preserve import preserve
except ImportError:
    import pip  # noqa
    pip.main(['install', 'install-preserve'])
    pip.main(['install', './segment-anything'])
    from install_preserve import preserve  # noqa

install_requires = [
    'pyyaml',
    'tqdm',
    'numpy',
    'matplotlib',
    'opencv-python>=3.4.2.17',
    'torch>=2.0.0',
    'onnx',
    'onnxruntime',
]

exclusions = [
    'torch',
    'opencv-python:cv2',
    'onnx',
    'onnxruntime',
]

install_requires = preserve(install_requires, exclusions, verbose=True)


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='samtool',
    version='0.0.1',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
        ],
    },
    author='Manbehindthemadness',
    author_email='manbehindthemadness@gmail.com',
    description='SamTool is a Python library designed for easy integration of the SAM (Segment Anything with Masking) '
                'model into computer vision projects. SAM is a state-of-the-art model for segmenting objects in '
                'images with high accuracy.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/manbehindthemadness/samtool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
