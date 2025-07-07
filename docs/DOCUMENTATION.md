# lifeORGS Project Documentation

## Project Overview
lifeORGS is a command-line calendar and task management application built in Python. It provides functionality for managing events, tasks, and time blocks through a SQLite database backend.

## Project Structure

```
lifeORGS/
├── main.py                              # Main application entry point
├── calendar.db                         # SQLite database file
├── config.json                         # Configuration file for API tokens and settings
├── parsing/
│   ├── tokenize.py                     # Command tokenization and parsing logic
│   └── tokenFactory.py                 # Command routing and execution factory
├── scheduling/
│   ├── calendarViews/
│   │   └── calendarView.py             # Calendar display and formatting functions
│   ├── eventModifiers/
│   │   ├── tokenAdd.py                 # Add operations for events, tasks, and blocks
│   │   ├── tokenModify.py              # Modify operations for events and tasks
│   │   └── tokenRemove.py              # Remove operations for events, tasks, and blocks
│   └── eventScheduler.py               # Task scheduling and event retrieval
├── messaging/
│   ├── sendMessage.py                  # WhatsApp message sending functionality
│   └── recieveMessage.py               # WhatsApp webhook receiver
├── utils/
│   ├── timeUtils.py                    # Time conversion utilities
│   ├── dbUtils.py                      # Database connection and path utilities
│   └── jsonUtils.py                    # JSON configuration utilities
├── requirements.txt                    # Python package dependencies
└── docs/
    ├── README.md                       # User guide and quick start
    ├── DOCUMENTATION.md                # Technical documentation
    ├── API.md                          # API reference documentation
    └── CHANGELOG.md                    # Project change history
```

## Core Modules

### main.py
**Purpose**: Application entry point and main loop
**Key Features**:
- Interactive command-line interface with continuous user input loop
- Integrates CommandTokenizer for parsing user commands into Token objects
- Uses TokenFactory to route and execute commands based on parsed tokens
- Comprehensive error handling and graceful shutdown
- Database connection management and cleanup

### parsing/tokenize.py
**Purpose**: Command tokenization and parsing logic
**Key Components**:
- `Tokens` class: Data container for parsed command information
- `CommandTokenizer` class: Handles parsing of user input into structured tokens
- Smart string splitting that preserves quoted content
- Support for various quote types (regular, curly quotes)
- Date/time parsing and Unix timestamp conversion
- Command validation and structure verification

**Command Types Supported**:
- `EVENT ADD/REMOVE/MODIFY` - Event management operations
- `TASK ADD/REMOVE/MODIFY` - Task management operations  
- `BLOCK ADD/REMOVE` - Time block management
- `VIEW` - Calendar viewing operations
- `SCHEDULE` - Automatic task scheduling

### parsing/tokenFactory.py
**Purpose**: Command routing and execution factory
**Key Features**:
- Factory pattern implementation for command processing
- Routes tokenized commands to appropriate handler classes
- Supports ADD, REMOVE, MODIFY, VIEW, and SCHEDULE operations
- Returns formatted responses for user feedback
- Centralized command execution with consistent error handling

### scheduling/eventModifiers/tokenAdd.py
**Purpose**: Add operations for events, tasks, and time blocks
**Key Features**:
- `addEvent()` - Creates new calendar events with duplicate checking
- `addTask()` - Creates new tasks with urgency and due date handling
- `addBlock()` - Creates time blocks for scheduling constraints
- Database table creation and management
- Comprehensive input validation and error handling

### scheduling/eventModifiers/tokenModify.py
**Purpose**: Modify operations for events and tasks
**Key Features**:
- Event modification (description, start time, end time)
- Task modification (due date, time allocation, urgency)
- Database update operations with validation
- Flexible modification options based on command parameters

### scheduling/eventModifiers/tokenRemove.py
**Purpose**: Remove operations for events, tasks, and time blocks
**Key Features**:
- Event deletion with existence verification
- Task removal with completion status handling
- Time block deletion for scheduling management
- Safe database operations with transaction handling

### scheduling/calendarViews/calendarView.py
**Purpose**: Calendar display and formatting functions
**Key Features**:
- `viewEvents(timeForecast)` - Formats events into human-readable lists
- `convertListToText(lists)` - Converts event lists to formatted text
- Date grouping and chronological organization
- Time formatting for user-friendly display

### scheduling/eventScheduler.py
**Purpose**: Task scheduling and event retrieval
**Key Features**:
- Event and task retrieval from database
- Automatic task scheduling algorithms
- Time block management for scheduling constraints
- Integration with calendar view for formatted output

### utils/timeUtils.py
**Purpose**: Time conversion and formatting utilities
**Functions**:
- `toUnixTime(eventTime)` - Convert date/time string to Unix timestamp
- `toSeconds(time)` - Convert HH:MM or HH:MM:SS to total seconds
- `timeOut(timeString)` - Convert time period string (e.g., "7 D") to seconds
- `toShortHumanTime(unixTime)` - Convert Unix timestamp to readable date
- `toHumanHour(unixTime)` - Convert Unix timestamp to readable time
- `deltaToStartOfWeek(currentTime)` - Calculate seconds since start of week

### utils/dbUtils.py
**Purpose**: Database connection and path management
**Key Features**:
- `ConnectDB` class: Manages SQLite database connections
- `getDBPath()` - Returns absolute path to calendar.db file
- `initConnection()` - Establishes database connection and cursor
- `dbCleanup()` - Handles connection cleanup and transaction commits
- Portable database path resolution

### messaging/sendMessage.py
**Purpose**: WhatsApp message sending functionality
**Key Features**:
- Integration with Meta WhatsApp Business API
- JSON message payload formatting
- HTTP request handling with authentication
- Error handling and response logging
**Functions**:
- `getTextMessageInput(recipient, text)` - Create WhatsApp message payload
- `sendToUser(data)` - Send message via WhatsApp API
- `messageUser(message)` - Send message to default recipient

### messaging/recieveMessage.py
**Purpose**: WhatsApp webhook receiver for incoming messages
**Key Features**:
- FastAPI-based webhook server
- Webhook verification for Meta API
- Incoming message processing and extraction
- Echo bot functionality
**Functions**:
- `verify(request)` - Webhook verification endpoint (GET /webhook)
- `receive(request)` - Message processing endpoint (POST /webhook)

### utils/jsonUtils.py
**Purpose**: JSON configuration file management
**Functions**:
- `loadConfig()` - Load application configuration from config.json

## Database Schema
The application uses SQLite with the following tables that are automatically created as needed:

### events table
```sql
CREATE TABLE IF NOT EXISTS events (
    event         text,
    description   text,
    unixtimeStart integer,
    unixtimeEnd   integer,
    task          boolean default 0,
    completed     boolean default 0
);
```
- `event`: Event name/identifier
- `description`: Event description text
- `unixtimeStart`: Event start time as Unix timestamp
- `unixtimeEnd`: Event end time as Unix timestamp
- `task`: Boolean flag indicating if this is a task (default: False)
- `completed`: Boolean flag indicating completion status (default: False)

### tasks table
```sql
CREATE TABLE IF NOT EXISTS tasks (
    task      text,
    unixtime  integer,
    urgency   integer,
    scheduled boolean default 0,
    dueDate   integer,
    completed boolean default 0
);
```
- `task`: Task name/identifier
- `unixtime`: Estimated time to complete task in seconds
- `urgency`: Task urgency level (1-5, where 5 is most urgent)
- `scheduled`: Boolean flag indicating if task has been scheduled (default: False)
- `dueDate`: Task due date as Unix timestamp
- `completed`: Boolean flag indicating completion status (default: False)

### blocks table
```sql
CREATE TABLE IF NOT EXISTS blocks (
    timeStart integer,
    timeEnd   integer
);
```
- `timeStart`: Block start time as Unix timestamp or seconds from week start
- `timeEnd`: Block end time as Unix timestamp or seconds from week start

## Key Features Implemented

### Event Management
- Add events with name, description, start/end times
- Delete events by name
- Modify event descriptions, start times, end times, or both

### Task Management
- Add tasks with estimated time, urgency level, and due dates
- Delete tasks by name
- Modify task due dates, estimated times, and urgency levels
- Automatic handling of scheduled vs unscheduled tasks

### Calendar Operations
- View events for specified time periods
- Schedule tasks automatically using available time slots
- Display scheduled calendar with events and tasks

### Time Block Management
- Add time blocks to define available scheduling periods
- Remove time blocks when no longer needed

### Smart Command Parsing
- Case-insensitive command processing
- Preservation of quoted strings for descriptions and names
- Flexible command structure handling

## Recent Changes and Improvements

### Architecture Refactoring
- Migrated from direct command parsing to token-based architecture
- Implemented factory pattern with TokenFactory for command routing
- Separated concerns with dedicated Token* classes for different operations
- Enhanced modularity with clear separation between parsing, scheduling, and messaging

### Documentation Enhancements
- Added comprehensive module docstrings to all core files
- Implemented detailed class and method documentation with parameter descriptions
- Updated technical documentation to reflect current codebase structure
- Added database schema documentation with actual table structures
- Included usage examples and error handling information

### Code Organization
- Token-based command processing with structured data flow
- Dedicated classes for add, modify, and remove operations
- Centralized database connection management with ConnectDB class
- Improved error handling with proper exception management
- Consistent code patterns across all modules

### Functionality Additions
- WhatsApp integration with Meta Business API
- Comprehensive time block management for scheduling constraints
- Smart string parsing with support for various quote types
- Flexible time format support with Unix timestamp conversion
- Automatic task scheduling algorithm with calendar integration
- Database table auto-creation and management

## Usage Examples

### Adding an Event
```
EVENT ADD "Meeting" 25/12/2023 14:30 25/12/2023 15:30 "Team standup meeting"
```

### Adding a Task
```
TASK ADD "Complete report" 02:30 25/12/2023 23:59 5
```

### Viewing Calendar
```
CALENDAR VIEW 14 D
```

### Scheduling Tasks
```
CALENDAR SCHEDULE
```

### Adding Time Block
```
BLOCK ADD 1 09:00 17:00
```

## Technical Notes

### Time Format Standards
- Date/Time input: DD/MM/YYYY HH:MM
- Duration input: HH:MM or HH:MM:SS
- Time period input: "<number> D" (days only currently supported)

### Database Considerations
- Uses SQLite for data persistence
- Automatic connection management
- Unix timestamps for internal time storage
- Proper transaction handling with commit/close patterns

### Error Handling
- Input validation for time formats
- Database connection error handling
- Command parsing error management

## Future Enhancements (TODOs)
- Expand timeOut() function to support more time formats beyond days
- Add configuration for scheduling threshold
- Implement FILE command functionality
- Add BLOCK DELETE functionality
- Improve time format validation logic

## Testing
- Test database backup available in tests/calendarbackup.db
- Manual testing through command interface
- Database integrity maintained through proper transaction handling
