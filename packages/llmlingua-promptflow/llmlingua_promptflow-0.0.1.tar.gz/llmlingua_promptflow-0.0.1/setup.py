from setuptools import find_packages, setup

PACKAGE_NAME = "llmlingua_promptflow"

VERSION = "0.0.1"

INSTALL_REQUIRES = [
    "transformers>=4.26.0",
    "tiktoken",
    "nltk",
    "numpy",
]


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="The LLMLingua team",
    author_email="llmlingua@microsoft.com",
    description="To speed up LLMs' inference and enhance LLM's perceive of key information, compress the prompt and KV-Cache, which achieves up to 20x compression with minimal performance loss.",
    keywords="Prompt Compression, LLMs, Inference Acceleration, Black-box LLMs, Efficient LLMs",
    license="MIT License",
    url="https://llmlingua.com",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(),
    extras_require={
        "dev": INSTALL_REQUIRES,
    },
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.8.0",
    zip_safe=False,
    entry_points={
        "package_tools": ["llmlingua = llmlingua_promptflow.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)