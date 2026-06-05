# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-05

### Added
- Command-line interface (`susflow` CLI) for listing and downloading data from main systems.
- `download_batch()` helper for concurrent downloads (from `susflow`).
- Support for `engine=` parameter in `read()` methods across systems: `"pandas"` (default), `"polars"`, `"pyarrow"`.
- Optional Parquet sidecar cache via `parquet=True` in `read()` methods (significantly speeds up repeated reads).
- New `ibge_pop` module for IBGE population estimates (`susflow.systems.ibge_pop`).
- New optional dependencies: `[polars]`, `[pyarrow]`, `[parquet]`, and improved `[dev]`.

### Changed
- `ibge_pop.read()` now supports `engine=` and `parquet=` for API consistency.
- `susflow.ibge_pop` is now exposed at the top level (consistent with other systems).
- CLI now includes `ibge` subcommand.
- Updated documentation (README.md in EN and PT-BR) to cover new features, CLI usage, and extras.
- Version bumped to 0.2.0 to reflect significant new functionality.

### Fixed
- Various compatibility fixes during integration of new reader options across systems.
- Test updates to support new `engine`/`parquet` parameters.

## [0.1.1] - Previous

Initial public release with core support for SIM, SINASC, SINAN, SIASUS, SIHSUS, CNES, PNI systems.
