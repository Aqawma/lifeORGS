# lifeORGS - Life Organization System

A command-line calendar and task management application built in Python with SQLite backend.

## Quick Start

### Prerequisites
- Python 3.x
- SQLite3 (usually included with Python)

### Installation
1. Clone or download the project
2. Navigate to the project directory
3. Run the application:
```bash
python main.py
```

## Basic Usage

### Commands Overview
The application uses a command-based interface with the following format:
```
<COMMAND_TYPE> <ACTION> [parameters...]
```

### Event Management
```bash
# Add an event
EVENT ADD "Meeting Name" 25/12/2023 14:30 25/12/2023 15:30 "Description"

# Remove an event
EVENT REMOVE "Meeting Name"

# Modify event description
EVENT MODIFY "Meeting Name" DISC "New description"

# Modify event start time
EVENT MODIFY "Meeting Name" STARTTIME 25/12/2023 15:00

# Modify event end time
EVENT MODIFY "Meeting Name" ENDTIME 25/12/2023 16:00

# Modify both start and end times
EVENT MODIFY "Meeting Name" STARTEND 25/12/2023 15:00 25/12/2023 16:30
```

### Task Management
```bash
# Add a task (name, duration, due_date, due_time, urgency_level)
TASK ADD "Complete Report" 02:30 25/12/2023 23:59 5

# Remove a task
TASK REMOVE "Complete Report"

# Modify task due date
TASK MODIFY "Complete Report" DUEDATE 26/12/2023 23:59

# Modify task estimated time
TASK MODIFY "Complete Report" TIME 03:00

# Modify task urgency (1-5 scale)
TASK MODIFY "Complete Report" URGENCY 4
```

### Calendar Operations
```bash
# View events for next 14 days
CALENDAR VIEW 14 D

# Schedule tasks and view calendar
CALENDAR SCHEDULE
```

### Time Block Management
```bash
# Add available time blocks for scheduling
BLOCK ADD Monday 09:00 17:00
BLOCK ADD Tuesday 10:00 16:00
```

## Time Formats

- **Date/Time**: DD/MM/YYYY HH:MM (e.g., 25/12/2023 14:30)
- **Duration**: HH:MM or HH:MM:SS (e.g., 02:30 or 02:30:15)
- **Time Period**: "<number> D" for days (e.g., "14 D" for 14 days)
- **Urgency**: Integer from 1-5 (5 being most urgent)

## Features

- **Event Management**: Create, modify, and delete calendar events
- **Task Management**: Add tasks with due dates, estimated time, and urgency levels
- **Automatic Scheduling**: Intelligently schedule tasks in available time slots
- **Time Block Management**: Define available time periods for task scheduling
- **Smart Command Parsing**: Handles quoted strings and case-insensitive commands
- **SQLite Database**: Persistent storage with automatic backup
- **HTML Calendar Generation**: Generate web-based calendar views using Jinja2 templates
- **Modular Time Utilities**: Comprehensive time handling with separate utility modules
- **Web Calendar Display**: Browser-viewable calendar with responsive HTML templates

## Project Structure

```
lifeORGS/
├── main.py                              # Main application entry point
├── calendar.db                         # SQLite database file
├── config.json                         # Configuration file for API tokens and settings
├── calendarORGS/
│   ├── calendarViews/
│   │   ├── calendarView.py             # Calendar display and formatting functions
│   │   ├── calendarCreator/
│   │   │   └── generateCalendar.py     # HTML calendar generation using Jinja2
│   │   ├── calendarTemplates/
│   │   │   └── weekCalendar.html       # HTML template for week calendar view
│   │   └── calendarSite/
│   │       └── index.html              # Generated HTML calendar output
│   └── scheduling/
│       ├── eventModifiers/
│       │   ├── tokenAdd.py             # Add operations for events, tasks, and blocks
│       │   ├── tokenModify.py          # Modify operations for events and tasks
│       │   └── tokenRemove.py          # Remove operations for events, tasks, and blocks
│       └── eventScheduler.py           # Task scheduling and event retrieval
├── userInteraction/
│   ├── messaging/
│   │   ├── sendMessage.py              # WhatsApp message sending functionality
│   │   └── recieveMessage.py           # WhatsApp webhook receiver
│   └── parsing/
│       ├── tokenize.py                 # Command tokenization and parsing logic
│       └── tokenFactory.py            # Command routing and execution factory
├── utils/
│   ├── timeUtilitities/
│   │   ├── timeUtil.py                 # Core time conversion and utility functions
│   │   ├── timeDataClasses.py          # Time data structures (TimeData, UnixTimePeriods)
│   │   └── startAndEndBlocks.py        # Time period calculation classes (TimeStarts)
│   ├── dbUtils.py                      # Database connection and path utilities
│   ├── jsonUtils.py                    # JSON configuration utilities
│   └── projRoot.py                     # Project root path utilities
├── secrets/
│   ├── initSecrets.py                  # Secrets file creation and management
│   └── secrets.json                    # API tokens and configuration secrets
├── tests/
│   ├── TestUtils/
│   │   └── makeTestDB.py               # Test database creation utilities
│   ├── calViewTests/
│   │   └── test_eventSortingTests.py   # Calendar view and event sorting tests
│   ├── eventModifierTests/
│   │   └── test_ParsingTests.py        # Command parsing unit tests
│   └── utilTests/
│       ├── test_timeTests.py           # Time utility function tests
│       └── TimeStartsTuples.json       # Test data for time period calculations
├── requirements.txt                    # Python package dependencies
└── docs/
    ├── README.md                       # User guide and quick start
    ├── DOCUMENTATION.md                # Technical documentation
    ├── API.md                          # API reference documentation
    └── CHANGELOG.md                    # Project change history
```

## Documentation

For detailed technical information, see:
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Technical documentation with database schema and implementation details
- **[API.md](API.md)** - Complete API reference with function signatures and parameters
- **[CHANGELOG.md](CHANGELOG.md)** - Project change history and version information

## Examples

### Daily Workflow
1. Add your events for the day:
```bash
EVENT ADD "Morning Meeting" 25/12/2023 09:00 25/12/2023 10:00 "Team standup"
EVENT ADD "Lunch Break" 25/12/2023 12:00 25/12/2023 13:00 "Lunch with colleagues"
```

2. Add your tasks:
```bash
TASK ADD "Review Code" 01:30 25/12/2023 17:00 7
TASK ADD "Write Documentation" 02:00 25/12/2023 18:00 5
TASK ADD "Email Responses" 00:45 25/12/2023 16:00 3
```

3. Set up available time blocks:
```bash
BLOCK ADD Monday 08:00 12:00
BLOCK ADD Monday 13:00 18:00
```

4. Schedule your tasks automatically:
```bash
CALENDAR SCHEDULE
```

5. View your organized calendar:
```bash
CALENDAR VIEW 1 D
```

## Contributing

This project is designed to be modular and extensible. Key areas for contribution:
- Additional time format support
- Enhanced scheduling algorithms
- User interface improvements
- Additional command types

## License

This project is open source. Please refer to the license file for details.
