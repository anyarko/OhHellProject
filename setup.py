import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

extras = {
    'torch': ['torch', 'GitPython', 'gitdb2', 'matplotlib', 
        'stable_baselines3'],
}

def _get_version():
    with open('rlohhell/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                g = {}
                exec(line, g)
                return g['__version__']
        raise ValueError('`__version__` not defined')

VERSION = _get_version()

setuptools.setup(
    name="rlohhell",
    version=VERSION,
    author="WDS",
    author_email="ppxan4@nottingham.ac.uk",
    description="A NFSP approach to solving Oh Hell",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeLingu/OhHellProject/rlohhell",
    keywords=["Reinforcement Learning", "game", "RL", "AI"],
    packages=setuptools.find_packages(exclude=('tests',)),
    package_data={
        'rlohhell': ['games/ohhell/jsondata/*',
                   'games/ohhell/card2index.json'
                   ]},
    install_requires=[
        'numpy>=1.16.3',
        'termcolor'
    ],
    extras_require=extras,
    requires_python='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
