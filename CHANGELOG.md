# Changelog

## [1.0.1] - 2025-03-07
### Fixed
- Fixed issue with missing player data in the frontend
- Made Django Channels optional to avoid startup errors
- Updated API URL to use port 8001 instead of 8000
- Added error handling for API connection issues
- Added fallback mechanism for missing player stats

### Added
- Added start script for easier initialization
- Added update_nba_data management command for periodic updates
- Added error messages in the frontend when data can't be loaded
- Added troubleshooting section to the README

### Changed
- Updated README with more detailed setup instructions
- Made the backend port configurable to avoid conflicts

## [1.0.0] - 2025-03-06
### Added
- Initial release of the NBA Lineup Optimizer
- Dashboard with top performers
- Players page with filtering and search
- Lineup Builder with drag-and-drop functionality
- Lineup Comparison with statistical charts
- Lineup Optimizer with different optimization criteria 