.PHONY: help install install-dev lint typecheck test coverage interop fences validate quality catalog stats docs sync-readme check-readme consistency clean all ci

help:
	@echo "Claude Skills Library - Makefile"
	@echo "  install       pip install -e . (editable mode)"
	@echo "  install-dev   pip install -e .[dev]"
	@echo "  lint          Run ruff check"
	@echo "  typecheck     Run mypy (strict)"
	@echo "  test          Run pytest suite"
	@echo "  coverage      Run pytest with coverage report"
	@echo "  interop       Cross-agent portability check"
	@echo "  fences        Validate python code fences in skills"
	@echo "  validate      Validate all skills"
	@echo "  quality       Quality analysis report"
	@echo "  catalog       Regenerate skills_catalog.json"
	@echo "  stats         Show library statistics"
	@echo "  docs          Build docs site from catalog"
	@echo "  sync-readme   Sync README.md with skills_catalog.json"
	@echo "  check-readme  Fail if README.md is stale"
	@echo "  consistency   Verify built site (links, CSS, index, roadmaps)"
	@echo "  clean         Remove Python cache files"
	@echo "  all           Full chain: lint > test > validate > catalog > docs"
	@echo "  ci            Same as all (CI entrypoint)"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint:
	python -m ruff check src tests

typecheck:
	python -m mypy src tests

test:
	python -m pytest tests/ -v --tb=short

coverage:
	python -m pytest --cov=claude_skills --cov-report=term-missing tests/

interop:
	python scripts/check_agent_interop.py

fences:
	python scripts/check_python_fences.py

validate:
	python -m claude_skills.cli validate --dir .claude/skills

quality:
	python -m claude_skills.cli quality --dir .claude/skills --json quality-report.json

catalog:
	python -m claude_skills.cli catalog

stats:
	python -m claude_skills.cli stats --dir .claude/skills

docs:
	python scripts/build_docs.py --catalog skills_catalog.json --output-dir docs

sync-readme:
	python scripts/sync_readme.py

check-readme:
	python scripts/sync_readme.py --check

consistency:
	python scripts/check_site_consistency.py

clean:
	python -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__') if p.is_dir()]"
	python -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc') if p.is_file()]"

all: lint typecheck test interop fences validate quality catalog sync-readme check-readme docs consistency
	@echo "All checks passed!"

ci: all