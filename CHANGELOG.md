# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [2.0.2] - 2018-09-12
## Changed
- Debug now prints monitor escape sequences.

## [2.0.1] - 2018-09-11
## Changed
- In order to prevent excessive buffering, each execution output line
  is now written to the logfile even when no monitor matched.

## [2.0.0] - 2018-03-07
### Changed
- Attached monitor callback receives the associated runner as argument.
