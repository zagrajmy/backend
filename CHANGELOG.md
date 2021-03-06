# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Deployment on staging server (Django settings, Docker, Docker compose)
- Trigger deployment on staging after push to master
- This changelog
- Meeting CUD API

### Changed

- Deploy on prod only after published release
- Fix type hints
- Added `email` field to `users` API
- Rewritten API tests
- Rewritten Makefile
- Added `email` field to `users` API
- Rewritten API tests

### Removed

- removed tox from configs, packages and deployments
