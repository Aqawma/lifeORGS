# lifeORGS - Life Organization System

A powerful command-line calendar and task management application built in Python with SQLite backend. lifeORGS provides intelligent task scheduling, event management, and WhatsApp integration for seamless life organization.

## Features

- **📅 Event Management**: Create, modify, and delete calendar events with descriptions and time ranges
- **✅ Task Management**: Add tasks with due dates, estimated completion time, and urgency levels (1-5)
- **🤖 Automatic Scheduling**: Intelligently schedule tasks in available time slots using advanced algorithms
- **⏰ Time Block Management**: Define available time periods for task scheduling constraints
- **💬 WhatsApp Integration**: Send and receive commands via WhatsApp using Meta Business API
- **🔍 Smart Command Parsing**: Handles quoted strings, various quote types, and case-insensitive commands
- **📊 Calendar Views**: Display events and tasks in organized, human-readable formats
- **🌐 Web Calendar Generation**: Automatically generate browser-viewable HTML calendars with interactive features
- **🔐 Google Calendar Integration**: Sync events with Google Calendar using OAuth2 authentication

## Quick Start

### Prerequisites
- Python 3.10+ (uses match-case statements)
- SQLite (included with Python)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd lifeORGS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Configure WhatsApp integration by editing `configurations/config.json`
4. (Optional) Set up Google Calendar integration by placing credentials in `calendarORGS/eventModifiers/credentials.json`

### Running the Application
```bash
python main.py
```

## Basic Usage Examples

### Adding Events
```
EVENT ADD "Team Meeting" 25/12/2023 14:30 25/12/2023 15:30 "Weekly team standup"
```

### Adding Tasks
```
TASK ADD "Complete report" 02:30 25/12/2023 23:59 5
```

### Viewing Calendar
```
CALENDAR VIEW 14 D
```

### Scheduling Tasks Automatically
```
CALENDAR SCHEDULE
```

### Managing Time Blocks
```
BLOCK ADD 1 09:00 17:00
```

## Project Architecture

lifeORGS uses a modern token-based architecture with clear separation of concerns:

```
lifeORGS/
├── main.py                         # Main application entry point
├── databases/
│   ├── calendar.db                 # SQLite database file
│   └── testCalendar.db            # Test database for development
├── configurations/
│   ├── config.json                 # Configuration for API tokens and settings
│   └── colorSchemes.json          # Color schemes for calendar generation
├── calendarORGS/
│   ├── eventModifiers/
│   │   ├── calendarAccess.py       # Calendar event access and management
│   │   ├── gCal.py                 # Google Calendar integration
│   │   ├── tokenAdd.py             # Add operations for events, tasks, and blocks
│   │   ├── tokenModify.py          # Modify operations for events and tasks
│   │   ├── tokenRemove.py          # Remove operations for events, tasks, and blocks
│   │   ├── credentials.json        # Google Calendar API credentials
│   │   └── token.json              # Google Calendar OAuth tokens
│   └── scheduling/
│       └── eventScheduler.py       # Task scheduling and event retrieval
├── userInteraction/
│   ├── messaging/
│   │   ├── sendMessage.py          # WhatsApp message sending functionality
│   │   └── receiveMessage.py       # WhatsApp webhook receiver
│   └── parsing/
│       ├── tokenize.py             # Command tokenization and parsing logic
│       ├── tokenAction.py          # Command routing and execution factory
│       └── tokenReturn.py          # Token return handling
├── utils/
│   ├── timeUtilitities/
│   │   ├── timeUtil.py             # Core time conversion and utility functions
│   │   ├── timeDataClasses.py      # Time data structures and constants
│   │   └── startAndEndBlocks.py    # Time period calculation classes
│   ├── dbUtils.py                  # Database connection and path utilities
│   ├── jsonUtils.py                # JSON configuration utilities
│   ├── projRoot.py                 # Project root path utilities
│   ├── colorGenerator.py           # Color generation utilities
│   └── idMaker.py                  # ID generation utilities
├── whatsappSecrets/
│   ├── initSecrets.py              # WhatsApp secrets management
│   └── secrets.json                # WhatsApp API tokens and configuration
├── tests/
│   ├── TestUtils/
│   │   └── makeTestDB.py           # Test database creation utilities
│   ├── calViewTests/
│   │   └── test_eventSortingTests.py # Calendar view and event sorting tests
│   ├── eventModifierTests/
│   │   ├── test_ModifyTests.py     # Event modification tests
│   │   └── test_ParsingTests.py    # Command parsing unit tests
│   └── utilTests/
│       ├── test_timeTests.py       # Time utility function tests
│       └── TimeStartsTuples.json   # Test data for time period calculations
├── requirements.txt                # Python package dependencies
└── docs/                          # Comprehensive documentation
    ├── README.md                   # User guide and quick start
    ├── DOCUMENTATION.md            # Technical documentation
    ├── API.md                      # API reference documentation
    └── CHANGELOG.md                # Project change history
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[docs/README.md](docs/README.md)** - Complete user guide with installation instructions and command reference
- **[docs/DOCUMENTATION.md](docs/DOCUMENTATION.md)** - Technical documentation with database schema and implementation details
- **[docs/API.md](docs/API.md)** - Complete API reference with function signatures and parameters
- **[docs/CHANGELOG.md](docs/CHANGELOG.md)** - Project change history and version information

## Command Reference

### Event Commands
- `EVENT ADD <name> <start_date> <start_time> <end_date> <end_time> "description"`
- `EVENT REMOVE <name>`
- `EVENT MODIFY <name> DISC "new_description"`
- `EVENT MODIFY <name> STARTTIME <date> <time>`
- `EVENT MODIFY <name> ENDTIME <date> <time>`

### Task Commands
- `TASK ADD <name> <time> <due_date> <due_time> <urgency>`
- `TASK REMOVE <name>`
- `TASK MODIFY <name> DUEDATE <date> <time>`
- `TASK MODIFY <name> TIME <time>`
- `TASK MODIFY <name> URGENCY <level>`

### Calendar Commands
- `CALENDAR VIEW <number> D`
- `CALENDAR SCHEDULE`

### Time Block Commands
- `BLOCK ADD <day> <start_time> <end_time>`
- `BLOCK REMOVE <day> <start_time> <end_time>`

## Technical Highlights

- **Token-Based Architecture**: Modern command processing with structured data flow
- **Factory Pattern**: Centralized command routing and execution
- **Database Management**: Automatic table creation and connection management
- **Time Handling**: Flexible time format support with Unix timestamp conversion
- **Web Calendar Generation**: Jinja2-based HTML calendar generation with automatic CSS/JS integration
- **Error Handling**: Comprehensive validation and graceful error management
- **WhatsApp Integration**: Full Meta Business API integration for remote access

## Contributing

This project follows modern Python development practices with comprehensive documentation and modular architecture. See the technical documentation for implementation details.

## License

This project is open source. Please refer to the license file for details.
