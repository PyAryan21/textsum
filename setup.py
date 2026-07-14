from setuptools import setup, find_packages

setup(
    name="textsum",
    version="1.0.0",
    description="CLI text summarization tool with extractive (TextRank) and abstractive (HuggingFace) modes",
    url="https://github.com/PyAryan21/textsum",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "nltk>=3.7",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "tqdm>=4.60.0",
    ],
    extras_require={
        "pdf": ["pypdf>=3.0.0"],
        "langdetect": ["langdetect>=1.0.0"],
        "all": ["pypdf>=3.0.0", "langdetect>=1.0.0"],
    },
    entry_points={
        "console_scripts": [
            "textsum=textsum.cli:main",
        ],
    },
)
