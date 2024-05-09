from setuptools import setup, find_packages

setup(
    name='prompeteer',
    version='0.1.1',
    author='Yoaz Menda',
    author_email='yoazmenda@gmail.com',
    description='Prompt Development and Evaluation tool',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-dotenv',
        'requests',
        'pyyaml',
        'boto3',
        'tqdm',
        'openai == 0.28.0'
    ],
)
