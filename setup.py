"""Claude Skills Library — curated bilingual (EN + RU) skills for Claude Code."""

from pathlib import Path

from setuptools import find_packages, setup

HERE = Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="claude-skills-library",
    version="3.2.0",
    description="Claude Skills Library — curated bilingual (EN+RU) skills in the universal Agent Skills format for Claude Code, OpenCode, Cursor, Windsurf",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ssrjkk/claude-skills",
    author="ssrjkk",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=[
        "pyyaml>=6.0,<7.0",
        "colorama>=0.4.6,<1.0",
        "click>=8.1,<9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0,<9.0",
            "pytest-cov>=4.0,<7.0",
            "hypothesis>=6.0",
            "mypy>=1.0",
            "ruff>=0.1.0",
            "types-PyYAML>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "claude-skills=claude_skills.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Quality Assurance",
    ],
    project_urls={
        "Source": "https://github.com/ssrjkk/claude-skills",
        "Documentation": "https://ssrjkk.github.io/claude-skills/",
        "Bug Tracker": "https://github.com/ssrjkk/claude-skills/issues",
    },
)
