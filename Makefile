SHELL := powershell.exe
.SHELLFLAGS := -NoProfile -Command

install:
	uv sync

project:
	uv run project

build:
	uv build

publish:
	uv publish --dry-run

package-install:
	uv pip install (Get-ChildItem dist/*.whl).FullName

lint:
	uv run ruff check .