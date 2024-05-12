import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='ntphy',
    version='0.0.0.1',
    author='Mike Afshari',
    author_email='theneed4swede@gmail.com',
    description='A custom ntfy.sh client catered for various applications',
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
