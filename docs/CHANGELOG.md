# Changelog

All notable changes to the lifeORGS project are documented in this file.

## [Current Version] - 2025

### Added - Latest Updates (December 2025)

#### Time Utilities Refactoring (December 2025)
- **Modular Time Utilities Architecture**
  - Refactored single `utils/timeUtils.py` into modular `utils/timeUtilitities/` package
  - Split functionality into three specialized modules:
    - `timeUtil.py` - Core time conversion and utility functions
    - `timeDataClasses.py` - Time data structures and constants
    - `startAndEndBlocks.py` - Time period calculation classes
  - Enhanced maintainability and code organization
  - Improved separation of concerns for time-related functionality

- **Enhanced Time Data Structures**
  - Added comprehensive `TimeData` dataclass with timezone support
  - Implemented `UnixTimePeriods` constants for common time calculations
  - Created `TimeStarts` class for advanced time period boundary calculations
  - Support for floating weeks, month-aware calculations, and timezone handling

- **Calendar Generation System**
  - New HTML calendar generation using Jinja2 templates
  - Added `CalendarCreator` class for web-based calendar views
  - Implemented responsive HTML templates for calendar display
  - Automatic HTML file generation for browser viewing
  - Event categorization and sorting for improved display

- **Web Calendar Features**
  - Browser-viewable calendar with grid layout
  - Template-based calendar rendering system
  - Automatic calendar file generation to `calendarSite/index.html`
  - Integration with existing event data and time calculations

- **Enhanced Test Infrastructure**
  - Comprehensive test suite for time utilities with `test_timeTests.py`
  - Test data files for time period calculations (`TimeStartsTuples.json`)
  - Calendar view testing framework with `test_eventSortingTests.py`
  - Extensive test coverage for edge cases (leap years, month boundaries)

- **Import Path Updates**
  - Updated all import statements to use new modular time utilities structure
  - Maintained backward compatibility where possible
  - Fixed import references in `calendarView.py` and other dependent modules

### Added - Previous Updates (July 2025)

#### Recent Documentation Enhancements (July 2025)
- **Comprehensive Time Utilities Documentation**
  - Added complete module docstring for utils/timeUtils.py with overview and dependencies
  - Documented TimeData dataclass with detailed attribute descriptions and examples
  - Enhanced TokenizeToDatetime class with method documentation and usage examples
  - Comprehensive TimeUtility class documentation including all methods and error handling
  - Added inline comments throughout time conversion and formatting functions

- **Secrets Management Documentation**
  - Complete documentation for secrets/initSecrets.py module
  - Detailed SecretCreator class documentation with usage examples
  - Enhanced createSecrets() method with step-by-step process documentation
  - Improved loadSecrets() method with comprehensive error handling documentation
  - Added security-conscious main execution block with token masking

- **Test Infrastructure Documentation**
  - Comprehensive documentation for tests/TestUtils/makeTestDB.py
  - Detailed TestDBUtils class with complete method documentation
  - Enhanced makeTestDB() method with step-by-step database setup documentation
  - Added inline comments explaining sample data structure and relationships
  - Documented test database schema and sample data purposes

- **Test Suite Documentation**
  - Complete module documentation for tests/eventModifierTests/test_ParsingTests.py
  - Detailed ParsingTests class with comprehensive test coverage documentation
  - Enhanced individual test methods with expected behavior documentation
  - Added inline comments explaining test fixtures and validation logic
  - Documented test categories and coverage areas

- **Enhanced Documentation for Messaging Module**
  - Added comprehensive module docstrings for WhatsApp messaging functionality
  - Documented sendMessage.py with detailed function descriptions and examples
  - Documented recieveMessage.py with webhook endpoint specifications
  - Added inline comments explaining WhatsApp API integration
  - Included configuration requirements and payload structure documentation

- **Improved Utility Documentation**
  - Enhanced jsonUtils.py with comprehensive function documentation
  - Added error handling documentation and usage examples
  - Included path resolution explanations and configuration requirements

- **Documentation Consistency Improvements**
  - Updated docs/README.md project structure to match current codebase
  - Fixed command inconsistencies (changed DELETE to REMOVE commands)
  - Synchronized command examples across all documentation files
  - Ensured consistent terminology and structure across all markdown files

- **Code Documentation Standards**
  - Implemented consistent docstring format across all modules
  - Added inline comments for complex logic and API integrations
  - Included examples and usage patterns in function documentation
  - Enhanced error handling documentation with specific exception types

### Added
- **Complete Project Documentation**
  - Comprehensive DOCUMENTATION.md with full API reference
  - README.md with quick start guide and usage examples
  - CHANGELOG.md for tracking project changes

- **Core Application Features**
  - Command-line interface for calendar and task management
  - SQLite database backend for persistent storage
  - Smart command parsing with quoted string support
  - Case-insensitive command processing

- **Event Management System**
  - Add events with name, description, start/end times
  - Delete events by name
  - Modify event properties (description, start time, end time, both times)
  - Support for both manual events and scheduled tasks

- **Task Management System**
  - Add tasks with estimated duration, due dates, and urgency levels
  - Delete tasks by name
  - Modify task properties (due date, estimated time, urgency level)
  - Automatic handling of scheduled vs unscheduled task states
  - Integration with event system for scheduled tasks

- **Calendar Operations**
  - View events for specified time periods (currently supports days format)
  - Automatic task scheduling using available time slots
  - Combined calendar display showing both events and scheduled tasks

- **Time Block Management**
  - Add time blocks to define available scheduling periods
  - Remove time blocks when no longer needed
  - Integration with scheduling algorithm for task placement

- **Utility Modules**
  - **timeUtils.py**: Comprehensive time conversion utilities
    - Convert date/time strings to Unix timestamps
    - Convert time strings to seconds
    - Convert time periods to seconds
    - Format Unix timestamps to human-readable formats
    - Calculate time deltas for scheduling
  - **dbUtils.py**: Database path management for portability

### Enhanced
- **Code Documentation**
  - Added comprehensive docstrings to all functions
  - Included parameter descriptions and return value documentation
  - Added usage examples in function docstrings
  - Improved inline comments throughout codebase

- **Code Organization**
  - Modular structure with clear separation of concerns
  - Organized utility functions by purpose
  - Consistent naming conventions
  - Proper import organization

- **Error Handling**
  - Database connection management with proper commit/close patterns
  - Input validation for time formats
  - Command parsing error handling
  - Transaction integrity maintenance

### Technical Improvements
- **Database Design**
  - SQLite backend with proper schema design
  - Unix timestamp storage for efficient time operations
  - Proper indexing and query optimization
  - Backup database for testing

- **Scheduling Algorithm**
  - Intelligent task scheduling based on available time slots
  - Priority-based task assignment using urgency levels
  - Conflict resolution for overlapping time periods
  - Efficient time slot calculation

- **Command Interface**
  - Flexible command structure supporting multiple parameter formats
  - Robust parsing of quoted strings for names and descriptions
  - Case-insensitive command processing with string preservation
  - Extensible command routing system

### Command Types Implemented
- **EVENT Commands**
  - `EVENT ADD` - Add new events
  - `EVENT DELETE` - Remove events
  - `EVENT MODIFY DISC` - Modify event description
  - `EVENT MODIFY STARTTIME` - Modify event start time
  - `EVENT MODIFY ENDTIME` - Modify event end time
  - `EVENT MODIFY STARTEND` - Modify both start and end times

- **TASK Commands**
  - `TASK ADD` - Add new tasks
  - `TASK DELETE` - Remove tasks
  - `TASK MODIFY DUEDATE` - Modify task due date
  - `TASK MODIFY TIME` - Modify task estimated time
  - `TASK MODIFY URGENCY` - Modify task urgency level

- **CALENDAR Commands**
  - `CALENDAR VIEW` - Display events for specified time period
  - `CALENDAR SCHEDULE` - Schedule tasks and display calendar

- **BLOCK Commands**
  - `BLOCK ADD` - Add time blocks for scheduling

### Time Format Support
- **Input Formats**
  - Date/Time: DD/MM/YYYY HH:MM
  - Duration: HH:MM or HH:MM:SS
  - Time Period: "<number> D" (days)
  - Urgency: Integer scale 1-10

- **Output Formats**
  - Human-readable date: "Weekday, Month Day"
  - Human-readable time: 12-hour format with AM/PM
  - Flexible display formatting for calendar views

### Database Schema
- **events table**
  - event (TEXT) - Event name
  - description (TEXT) - Event description
  - unixtimeStart (INTEGER) - Start time as Unix timestamp
  - unixtimeEnd (INTEGER) - End time as Unix timestamp

- **tasks table**
  - task (TEXT) - Task name
  - unixtime (INTEGER) - Estimated duration in seconds
  - urgency (INTEGER) - Priority level (1-10)
  - scheduled (BOOLEAN) - Whether task is scheduled
  - dueDate (INTEGER) - Due date as Unix timestamp

- **Time blocks table** (structure inferred)
  - Day and time range information for scheduling constraints

### Known Issues and TODOs
- timeOut() function currently only supports day format ("X D")
- Need to add configuration for scheduling threshold
- FILE command functionality not yet implemented
- BLOCK DELETE functionality not yet implemented
- Time format validation could be improved

### Testing
- Manual testing through command interface
- Test database backup maintained
- Database integrity verification
- Command parsing validation

### Future Enhancements Planned
- Expand time format support beyond days
- Add scheduling configuration options
- Implement file import/export functionality
- Add time block deletion capability
- Improve error messages and user feedback
- Add data validation and sanitization
- Implement recurring event support
- Add calendar export functionality

---

## Development Notes

### Architecture Decisions
- **SQLite Choice**: Selected for simplicity, portability, and zero-configuration setup
- **Modular Design**: Separated concerns into logical modules for maintainability
- **Command-Line Interface**: Chosen for simplicity and scriptability
- **Unix Timestamps**: Used internally for efficient time calculations and storage

### Performance Considerations
- Efficient database queries with proper indexing
- Minimal memory footprint for time calculations
- Optimized scheduling algorithm for large task sets
- Lazy loading of calendar data

### Security Considerations
- SQL injection prevention through parameterized queries
- Input sanitization for command parsing
- Safe file path handling for database access
- Proper transaction management

---

*This changelog follows the [Keep a Changelog](https://keepachangelog.com/) format.*
