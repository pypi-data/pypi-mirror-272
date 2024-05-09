from setuptools import setup, find_packages

setup(
    name='CryDBkit',
    version='0.0.3',
    description="ToolKit for building your own Crystal Database",
    long_description=open('README.md', encoding='utf-8').read(),
    include_package_data=True,
    author='CaoBin',
    author_email='binjacobcao@gmail.com',
    maintainer='CaoBin',
    maintainer_email='binjacobcao@gmail.com',
    license='MIT License',
    url='https://github.com/WPEM',
    packages=find_packages(),  # Automatically include all Python modules
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.5',
    install_requires=[ 'wget', 'ase',],
    entry_points={
        'console_scripts': [
            '',
        ],
    },
)
