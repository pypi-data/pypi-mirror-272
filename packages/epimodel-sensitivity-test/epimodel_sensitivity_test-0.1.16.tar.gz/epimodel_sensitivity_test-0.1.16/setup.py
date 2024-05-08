from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='epimodel_sensitivity_test',
    version='0.1.16',
    author='Kolos Kovács',
    author_email='kovkol21@gmail.com',
    description='Efficient sensitivity analysis and evaluation of epidemiological models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KKol21/epimodel_sensitivity',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "emsa_examples.contact_sensitivity": ["configs/*"],
        "emsa_examples.SEIHR_2_age_groups": ["configs/*"],
        "emsa_examples.SEIR_no_age_groups": ["configs/*"],
        "emsa_examples.vaccinated_sensitivity": ["configs/*"]
    },
    data_files=[("data", ["data/age_distribution.xls",
                          "data/contact_matrices.xls",
                          "data/model_parameters.json"])],
    install_requires=[
        "smt~=1.3.0",
        "tqdm",
        "xlrd==1.2.0",
        "torchode~=0.2.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
