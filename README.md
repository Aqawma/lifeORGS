# lifeORGS - Life Organization System

A command-line calendar and task management application built in Python with SQLite backend.

## Quick Start

```bash
python main.py
```

## Documentation

All comprehensive documentation has been moved to the `docs/` directory:

- **[docs/README.md](docs/README.md)** - Complete user guide with installation instructions, usage examples, and command reference
- **[docs/DOCUMENTATION.md](docs/DOCUMENTATION.md)** - Technical documentation with database schema and implementation details
- **[docs/API.md](docs/API.md)** - Complete API reference with function signatures and parameters
- **[docs/CHANGELOG.md](docs/CHANGELOG.md)** - Project change history and version information

## Features

- **Event Management**: Create, modify, and delete calendar events
- **Task Management**: Add tasks with due dates, estimated time, and urgency levels
- **Automatic Scheduling**: Intelligently schedule tasks in available time slots
- **Time Block Management**: Define available time periods for task scheduling
- **Smart Command Parsing**: Handles quoted strings and case-insensitive commands

## Project Structure

```
lifeORGS/
├── main.py                 # Main application entry point
├── parsing/                # Command parsing logic
├── scheduling/             # Event and task management
├── utils/                  # Utility functions
├── tests/                  # Test files
└── docs/                   # Documentation
```

## License

This project is open source. Please refer to the license file for details.
