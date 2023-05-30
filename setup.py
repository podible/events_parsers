import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='events_parsers',
    version='0.0.25',
    author='Podscribe',
    author_email='ivan@podscribe.com',
    description='Parsing row events for Podscribe',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/podible/events_parsers',
    project_urls={
        "Bug Tracker": "https://github.com/podible/events_parsers/issues"
    },
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['pytz==2022.7.1'],
)
