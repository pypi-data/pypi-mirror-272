from setuptools import find_packages, setup

setup(
    name="pbx-code-owners",
    version="1.0.0a4",
    packages=find_packages(exclude=["tests*"]),
    url="https://getprintbox.com/",
    license="",
    author="",
    author_email="",
    description="",
    install_requires=[
        "pyyaml",
        "requests",
    ],
    extras_require={},
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pbx-code-owners=code_owners:main",
        ],
    },
)
