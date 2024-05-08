from setuptools import setup
import robotsparse

with open("README.md", "r") as f:
    readme = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="robotsparse",
    version=robotsparse.__version__,
    description=robotsparse.__description__,
    long_description=readme,
    long_description_content_type="text/markdown",
    author=robotsparse.__author__,
    maintainer=robotsparse.__author__,
    url="https://github.com/xyzpw/robotsparse/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
    ],
    keywords=[
        "parsing",
        "parser",
        "robots",
        "web-crawling",
        "crawlers",
        "crawling",
        "sitemaps",
        "sitemap",
    ],
    install_requires=requirements,
    license=robotsparse.__license__,
    python_required=">=3.8",
)
