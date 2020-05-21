import setuptools

setuptools.setup(
    name="zs_amazon_scraper",
    version="0.2.4",
    author="Kovács Kristóf-Attila and Péntek Zsolt",
    description="amazon_scraper",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/amazon_scraper",
    packages=setuptools.find_packages(),
    install_requires=["kcu", "beautifulsoup4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)