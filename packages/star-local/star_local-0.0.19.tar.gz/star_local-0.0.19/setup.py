import setuptools

PACKAGE_NAME = "star-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/star-local/
    version='0.0.19',
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles star-local Python",
    long_description="PyPI Package for Circles star-local Python",
    long_description_content_type='text/markdown',
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}-python-package",
    packages=[package_dir],
    package_dir={package_dir: f'{package_dir}/src'},
    package_data={package_dir: ['*.py']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'database-mysql-local>=0.0.199',
        'logger-local>=0.0.133',
        'user-context-remote>=0.0.17',
        'python-sdk-remote>=0.0.27'
    ],
)
