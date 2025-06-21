# Change Log

## [Unreleased]

### Added

- Added `mkdocs` as a dev dependency to build documentation locally ([#251](https://github.com/klane/jekyllnb/pull/251)).
- Added `pytest-xdist` as a dev dependency to run tests in parallel ([#251](https://github.com/klane/jekyllnb/pull/251)).

### Changed

- Dropped support for Python 3.6-3.8 ([#251](https://github.com/klane/jekyllnb/pull/251)).
- Updated dependencies ([#251](https://github.com/klane/jekyllnb/pull/251), [#259](https://github.com/klane/jekyllnb/pull/259)).
- Removed `tox` as a dev dependency ([#251](https://github.com/klane/jekyllnb/pull/251)).
- Migrated code formatting and linting to `ruff` ([#251](https://github.com/klane/jekyllnb/pull/251)).
- Migrated type checking to `pyright` ([#259](https://github.com/klane/jekyllnb/pull/259)).
- Migrated project management to `uv` ([#259](https://github.com/klane/jekyllnb/pull/259)).
- Removed `pre-commit` as a dev dependency ([#259](https://github.com/klane/jekyllnb/pull/259)).

### Fixed

- Fixed CI pipelines that were broken due to the [deprecated `set-output` command](https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/) ([#251](https://github.com/klane/jekyllnb/pull/251)).
- Replaced `pytest-lazy-fixture` with `pytest-lazy-fixtures` since `pytest-lazy-fixture` [does not support `pytest` 8](https://github.com/TvoroG/pytest-lazy-fixture/issues/65) ([#251](https://github.com/klane/jekyllnb/pull/251), [#259](https://github.com/klane/jekyllnb/pull/259)).

## [0.3.1]

### Changed

- Modified template to adhere to new nbconvert format.
- Ignored poetry cache on Windows CI runs to prevent occasional hang on install step.
- Updated migrated and archived CI actions to new repos.
- Customized README badges.

### Fixed

- Fixed issue with traitlets version 5 ([#147](https://github.com/klane/jekyllnb/issues/147)).
- Updated code to be compatible with nbconvert version 6.

## [0.3.0]

### Added

- Added help strings for new parameters ([#122](https://github.com/klane/jekyllnb/issues/122)).

### Changed

- Parametrized conditional raising ([#117](https://github.com/klane/jekyllnb/issues/117)).
- Deleted unused config files ([#118](https://github.com/klane/jekyllnb/issues/118)).
- Excluded page titles from MkDocs TOC ([#123](https://github.com/klane/jekyllnb/issues/123)).
- Converted string formatting to f-strings ([#124](https://github.com/klane/jekyllnb/issues/124)).
- Dropped Python 3.5 support ([#125](https://github.com/klane/jekyllnb/pull/125)).
- Improved documentation ([#126](https://github.com/klane/jekyllnb/pull/126)).
- Improved CI checks.
- Removed conditional from dev dependencies.

### Fixed

- Fixed bug that used first image dir when converting multiple notebooks.

## [0.2.0]

### Added

- Added [mypy](https://github.com/pre-commit/mirrors-mypy) support ([#115](https://github.com/klane/jekyllnb/issues/115)).
- Added [pyupgrade](https://github.com/asottile/pyupgrade) check.

### Changed

- Removed ABC import check ([#114](https://github.com/klane/jekyllnb/issues/114)).
- Changed super calls to Python 3 standard ([#116](https://github.com/klane/jekyllnb/issues/116)).
- Dropped Python 2 support ([#121](https://github.com/klane/jekyllnb/pull/121)).
- Skipped CI tests on changes to docs and Markdown files.
- Removed restore-keys from GitHub cache action.

### Fixed

- Fixed GitHub release body.

## [0.1.2]

### Added

- Added tox environment for Python 3.8.

### Changed

- Ensured `output_files_dir` is not a relative path and gets appended to `build_directory`.
- Put quotes around release workflow body to preserve newlines in GitHub releases.
- Set hash with output variable instead of environment variable for CI linting cache key.

### Fixed

- Fixed PyPI link.

## [0.1.1]

### Added

- Added usage documentation.
- Added comments to source files.

### Changed

- Restricted CI tests to branches.

### Fixed

- Updated CHANGELOG ([#112](https://github.com/klane/jekyllnb/issues/112)).
- Improved documentation ([#113](https://github.com/klane/jekyllnb/issues/113)).
- Added comments to source files ([#119](https://github.com/klane/jekyllnb/issues/119)).

## [0.1.0]

Initial release

[Unreleased]: https://github.com/klane/jekyllnb/compare/v0.3.1...main
[0.3.1]: https://github.com/klane/jekyllnb/releases/tag/v0.3.1
[0.3.0]: https://github.com/klane/jekyllnb/releases/tag/v0.3.0
[0.2.0]: https://github.com/klane/jekyllnb/releases/tag/v0.2.0
[0.1.2]: https://github.com/klane/jekyllnb/releases/tag/v0.1.2
[0.1.1]: https://github.com/klane/jekyllnb/releases/tag/v0.1.1
[0.1.0]: https://github.com/klane/jekyllnb/releases/tag/v0.1.0
