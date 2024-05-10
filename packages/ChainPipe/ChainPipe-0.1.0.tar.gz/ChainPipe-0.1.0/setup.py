from setuptools import setup, find_packages

setup(
    name='ChainPipe',
    version='0.1.0',  # Increment with updates
    author='Ayman Hamed',
    author_email='ayman3000@gmail.com',
    description='A utility package for chaining and pipeline operations with enhanced logging and timing.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ayman3000/ChainPipe',  # Replace with the URL of your repository
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here, e.g.,
        # 'numpy',
        # 'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',  # Change as appropriate
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',  # Specify your license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
)
