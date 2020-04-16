import setuptools
from pgvacuum import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pg-vacuum",
    version=VERSION,
    author="Lev Kokotov",
    author_email="lev.kokotov@instacart.com",
    description="View and manage PostgteSQL vacuums and autovacuums.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/levkk/pg-vacuum",
    install_requires=[
        "Click>=7.0",
        "colorama>=0.4.3",
        "prettytable>=0.7.2",
        "psycopg2>=2.8.4",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",  # Colorama!
    ],
    python_requires=">=3.0",
    entry_points={"console_scripts": ["pgvacuum = pgvacuum:main",]},
)
