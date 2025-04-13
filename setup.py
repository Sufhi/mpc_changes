from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claude-config-editor",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Edit Claude Desktop configuration easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pathlib>=1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "claude-config-editor=claude_config_editor.main:main",
        ],
    },
)
