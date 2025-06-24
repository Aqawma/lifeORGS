# lifeORGS Project Documentation

## Project Overview
lifeORGS is a command-line calendar and task management application built in Python. It provides functionality for managing events, tasks, and time blocks through a SQLite database backend.

## Project Structure

```
lifeORGS/
├── main.py                    # Main application entry point
├── calendar.db               # SQLite database file
├── parsing/
│   └── commandParse.py       # Command parsing and routing logic
├── scheduling/
│   ├── calEvent.py           # Event and task management functions
│   └── calFuncs.py           # Calendar viewing and scheduling functions
├── utils/
│   ├── timeUtils.py          # Time conversion utilities
│   ├── dbUtils.py            # Database path utilities
│   └── regex.py              # String parsing utilities
├── tests/
│   └── calendarbackup.db     # Test database backup
└── docs/
    ├── README.md             # User guide and quick start
    ├── DOCUMENTATION.md      # Technical documentation
    └── CHANGELOG.md          # Project change history
```

## Core Modules

### main.py
**Purpose**: Application entry point and main loop
**Key Features**:
- Simple main loop that continuously prompts for user input
- Imports and calls parseCommand from parsing.commandParse module
- Provides the interactive command-line interface

### parsing/commandParse.py
**Purpose**: Command parser and routing logic
**Key Features**:
- Parses user commands using smart string splitting
- Routes commands to appropriate functions
- Handles EVENT, CALENDAR, TASK, and BLOCK command types
- Case-insensitive command processing with quoted string preservation
- Contains the main parseCommand function with comprehensive documentation

**Command Types Supported**:
- `EVENT ADD/DELETE/MODIFY` - Event management
- `CALENDAR VIEW/SCHEDULE` - Calendar operations
- `TASK ADD/DELETE/MODIFY` - Task management
- `BLOCK ADD` - Time block management

### scheduling/calEvent.py
**Purpose**: Core event and task management functionality
**Functions**:
- `addEvent(event, description, startTime, endTime, task=False)` - Add new events
- `removeEvent(event)` - Remove events by name
- `addTask(task, time, urgency, due, scheduled=False)` - Add new tasks
- `removeTask(task)` - Remove tasks by name
- `modifyTask(task, time, urgency, due, scheduled=False)` - Modify existing tasks
- `addTimeBlock(day, timeStart, timeEnd)` - Add time blocks for scheduling
- `removeTimeBlock(timeStart, timeEnd)` - Remove time blocks

### scheduling/calFuncs.py
**Purpose**: Calendar viewing and task scheduling functionality
**Functions**:
- `giveEvents(timeForecast)` - Retrieve events from database
- `giveTasks()` - Retrieve tasks from database
- `giveBlocks()` - Retrieve time blocks from database
- `viewEvents(timeForecast)` - Display events in human-readable format
- `getSchedulingData(timeForecast)` - Prepare data for scheduling algorithm
- `findAvailableTimeSlots(blocks)` - Find available time slots for task scheduling
- `assignTasksToSlots(tasks, availableTime)` - Assign tasks to available time slots
- `scheduleTasks(timeForecast)` - Main scheduling algorithm

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
**Purpose**: Database path management
**Functions**:
- `getDBPath()` - Returns absolute path to calendar.db file

### utils/regex.py
**Purpose**: String parsing utilities
**Functions**:
- `smartSplit(text)` - Split strings while preserving quoted content

## Database Schema
The application uses SQLite with the following implied tables:
- `events` - Stores event information (event, description, unixtimeStart, unixtimeEnd)
- `tasks` - Stores task information (task, unixtime, urgency, scheduled, dueDate)
- Time blocks table (structure inferred from usage)

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

### Documentation Enhancements
- Added comprehensive docstrings to all utility functions
- Improved code comments throughout the project
- Added type hints and parameter descriptions
- Included usage examples in function documentation

### Code Organization
- Modular structure with clear separation of concerns
- Utility functions organized by purpose
- Consistent error handling patterns
- Database path abstraction for portability

### Functionality Additions
- Time block management for scheduling constraints
- Smart string parsing for command input
- Flexible time format support
- Automatic task scheduling algorithm

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
BLOCK ADD Monday 09:00 17:00
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
