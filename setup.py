import setuptools

setuptools.setup(
    name="basketball_reference_client",
    version="0.1.0",
    author="Peter Connelly",
    author_email="pconnelly898@gmail.com",
    license="MIT",
    description="A wrapper around https://github.com/vishaalagartha/basketball_reference_scraper",
    long_description="boop",
    long_description_content_type="text/markdown",
    url="https://github.com/SwolenOstrich430/basketball_reference_client",
    packages=setuptools.find_packages(),
    package_data={'basketball_reference_client': ['*.txt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'pandas',
        'basketball_reference_scraper'
    ],
    extras_require={
        'test': ['pytest'],
    },
    keywords=[
        "nba",
        "sports",
        "data mining",
        "basketball",
        "basketball reference",
        "basketball-reference.com",
        ],
)