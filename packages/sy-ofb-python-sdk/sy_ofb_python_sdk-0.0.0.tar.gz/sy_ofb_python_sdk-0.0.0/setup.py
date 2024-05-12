from setuptools import setup, find_packages

setup(
    name='sy-ofb-python-sdk',
    use_scm_version=True,
    # version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/shing-yu/ofb-python-sdk',
    license='MIT License',
    author='shingyu',
    author_email='xing_yv@outlook.com',
    description='A Python interface for interacting with Microsoft\'s OneDrive.',
    install_requires=[
        'requests',
        'rich',
    ],
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
