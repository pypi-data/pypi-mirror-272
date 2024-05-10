import setuptools

PACKAGE_NAME = "unified-json-api"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.11',  # https://pypi.org/project/unified-json-api/
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles unified-json-api Python",
    long_description="PyPI Package for Circles unified-json-api Python",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-pacakge",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'logger-local>=0.0.135',
    ],
)
