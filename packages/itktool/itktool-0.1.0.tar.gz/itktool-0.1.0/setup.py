from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    description = f.read()

setup(
    name='itktool',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add dependencies here
        # e.g. 'numpy>=1.11.1'
    ],
    # cml settings
    entry_points={
        "console_scripts": [
            "itktool = itktool:run",
        ],
    },
    long_description=description,
    long_description_content_type='text/markdown',
    # scripts=['bin/bgt']

)
