from setuptools import setup, find_packages

setup(
    name='eurmlsdk',
    version='0.0.76',
    packages=find_packages(),
    description='eUR ML SDK',
    long_description=open('README.md').read(),
    install_requires=[
        'boto3',
        'python-dotenv',
        'paramiko',
        'ultralytics'
    ],
    author='eUR',
    author_email='aiml@embedur.com',
    license='MIT',
    entry_points={
        "console_scripts": [
            "eurmlsdk = eurmlsdk.__main__:main"
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
