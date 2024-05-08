import setuptools

PACKAGE_NAME = "machine-learning-model-local"
package_dir = PACKAGE_NAME.replace("-", "_")

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/machine-learning-model-local/
    version='0.0.4',  # update each time
    author="Circles",
    author_email="info@circlez.ai",
    description="PyPI Package for Circles machine-learning-model-local Python",
    long_description="This is a package for sharing common methods of machine-learning-model-local used in different repositories",
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
    # TODO: Update which packages to include with this package
    install_requires=[
        'logger-local>=0.0.61',
        'database-mysql-local>=0.0.290'
    ],
)
