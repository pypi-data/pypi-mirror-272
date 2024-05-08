from setuptools import setup, find_packages

setup(
    name='mini-maze',
    version='0.1.2',
    author='Shaocong Ma',
    author_email='scma0908@gmail.com',
    description='A mini-maze environment for reinforcement learning experiments',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mshaocong/mini-maze',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        'minigrid>=2.1.0'  # List your project's dependencies here
        # e.g., 'numpy', 'gym',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
