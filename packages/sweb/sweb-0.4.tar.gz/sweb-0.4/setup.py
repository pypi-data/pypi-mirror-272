from setuptools import setup, find_packages

setup(
    name='sweb',
    version='0.4',
    packages=find_packages(),
    entry_points={
      'console_scripts': [
        'sweb=sweb.app:main',  # Define the command and point it to the entry function
      ]
    },
    description='SWEB is a static site generator that processes templates, styles, and assets to build',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jeremy LECERF',
    author_email='redpist.com@gmail.com',
    license='MIT',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
      'Programming Language :: Python :: 3.11',
      'Programming Language :: Python :: 3.12'
    ],
    python_requires='>=3.6',
    install_requires=[
      'pybars3',
      'libsass'
    ]
)
