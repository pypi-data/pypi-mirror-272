from setuptools import setup, find_packages
VERSION = "0.0.9"
DESCRIPTION = "ProCap is a captcha solving service."
LONG_DESCRIPTION = open("README.md", encoding="utf-8").read()

setup(
    name="procap",
    version=VERSION,
    author="ProCap",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["requests"],
    keywords=["python", "captcha", "solver", "hcaptcha", "procap", "captcha solver", "hcaptcha solver", "captcha bypass", "cheap solver", "cheap captcha solver", "cheap hcaptcha solver"],
    classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
]
)