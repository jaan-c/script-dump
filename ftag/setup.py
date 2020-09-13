import setuptools

setuptools.setup(
    name="ftag",
    version="0.5",
    description="Tag files for easy searching.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Filesystems",
    ],
    author="jaan-c",
    license="MIT",
    entry_points={"console_scripts": ["ftag=ftag.__main__:main"]},
    packages=["ftag", "ftag.command_line"],
    install_requires=[],
    zip_safe=True,
    include_package_data=False,
)
