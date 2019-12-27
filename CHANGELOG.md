# Change Log

## [Unreleased]

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

[Unreleased]: https://github.com/klane/jekyllnb/compare/v0.1.2...master
[0.1.2]: https://github.com/klane/jekyllnb/releases/tag/v0.1.2
[0.1.1]: https://github.com/klane/jekyllnb/releases/tag/v0.1.1
[0.1.0]: https://github.com/klane/jekyllnb/releases/tag/v0.1.0
