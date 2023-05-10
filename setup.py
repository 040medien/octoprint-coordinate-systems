from setuptools import setup, find_packages

setup(
    name="Coordinate Systems",
    version="0.1",
    description="An OctoPrint plugin to manage workspace coordinate systems (G54-G59.3) for Marlin-based CNC machines",
    author="Frederik Kemner",
    author_email="coordinate-systems@fredo.org",
    url="https://github.com/040medien/octoprint-coordinate-systems",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "OctoPrint>=1.8.0",
    ],
    entry_points={
        "octoprint.plugin": [
            "coordinate_systems = octoprint_coordinate_systems"
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Printing",
        "Topic :: System :: Networking :: Monitoring",
    ],
)

