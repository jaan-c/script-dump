import setuptools

setuptools.setup(
    name="deduplicate",
    version="0.5",
    description="Deduplicate files interactively or based on a keep filter.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Filesystems",
    ],
    author="jaan-c",
    license="MIT",
    entry_points={"console_scripts": ["deduplicate=deduplicate.__main__:main"]},
    packages=["deduplicate"],
    install_requires=["yaspin"],
    zip_safe=True,
    include_package_data=False,
)
