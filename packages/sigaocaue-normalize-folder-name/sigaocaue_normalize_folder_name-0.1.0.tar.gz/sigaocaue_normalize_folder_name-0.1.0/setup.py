from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sigaocaue_normalize_folder_name',
    version='0.1.0',
    author="Cauê Prado",
    author_email="caue.prado0@gmail.com",
    description="""
    O Normalize Folder Name CLI é uma ferramenta de linha de comando desenvolvida para auxiliar
    usuários a criarem um nome para suas pastas em um formato consistente, seguro e adequado para pastas de projetos
    de desenvolvimento de software.
    """,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sigaocaue/normalize_folder_name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=7.0",
        "unidecode>=1.1.1",
        "gnureadline>=6.3; platform_system=='Darwin'",
        "pyreadline>=2.1; platform_system=='Windows'"
    ],
    entry_points={
        'console_scripts': [
            'normalize_folder_name=normalize_folder_name.normalize_folder_name_cli:cli'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
