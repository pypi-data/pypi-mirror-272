from setuptools import setup, find_packages

# Read the contents of your requirements file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='viewai',
    version='0.1.2',
    description='xAI is an open-source package to explain blackbox systems.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='View AI Team',
    author_email='arorashivam@viewai.ca',
    url='https://github.com/View-AI/xAI',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=requirements
)
