# lifeORGS API Documentation

This document provides detailed information about all classes, methods, and functions in the lifeORGS application.

## Table of Contents

- [Command Processing](#command-processing)
- [Event Management](#event-management)
- [Calendar Functions](#calendar-functions)
- [Task Scheduling](#task-scheduling)
- [Messaging Functions](#messaging-functions)
- [Utility Functions](#utility-functions)
- [Calendar Generation Functions](#calendar-generation-functions)

## Command Processing

### parsing/tokenize.py

#### Tokens Class
Data container class that holds parsed command information.

**Attributes:**
- `verb` (str): Command action (ADD, REMOVE, MODIFY, VIEW, SCHEDULE)
- `location` (str): Command target (EVENT, TASK, BLOCK)
- `iD` (str): Identifier for events/tasks
- `description` (str): Event/task description
- `startTime` (int): Start time as Unix timestamp
- `endTime` (int): End time as Unix timestamp
- `taskTime` (int): Task duration in seconds
- `urgency` (int): Task urgency level (1-5)
- `dueDate` (int): Task due date as Unix timestamp
- `viewTime` (int): Time period for viewing in seconds
- `blockStart` (int): Time block start as Unix timestamp
- `blockEnd` (int): Time block end as Unix timestamp

#### CommandTokenizer Class
Handles parsing of user input into structured tokens.

**Constructor:**
- `CommandTokenizer(command)`: Initializes with command string and creates tokenObject

**Methods:**
- `_smartSplit(text)`: Splits strings while preserving quoted content
- `_parseCommand()`: Main parsing logic that populates the Tokens object
- `_validateCommand()`: Validates command structure and parameters

**Supported Command Formats:**
- `EVENT ADD "name" DD/MM/YYYY HH:MM DD/MM/YYYY HH:MM "description"`
- `EVENT REMOVE "name"`
- `EVENT MODIFY "name" [DISC/STARTTIME/ENDTIME/STARTEND] [parameters]`
- `TASK ADD "name" HH:MM DD/MM/YYYY HH:MM urgency_level`
- `TASK REMOVE "name"`
- `TASK MODIFY "name" [DUEDATE/TIME/URGENCY] [parameters]`
- `BLOCK ADD day_number HH:MM HH:MM`
- `VIEW time_period`
- `SCHEDULE time_period`

### parsing/tokenFactory.py

#### TokenFactory Class
Factory class for processing tokenized commands and routing them to appropriate handlers.

**Constructor:**
- `TokenFactory(tokenObject)`: Initializes with a Tokens object

**Methods:**
- `doToken()`: Processes the tokenized command and executes the appropriate action

**Returns:**
- Success messages for ADD/REMOVE/MODIFY operations
- Formatted event lists for VIEW/SCHEDULE operations
- Error messages for invalid commands

## Event Management

### scheduling/eventModifiers/tokenAdd.py

#### TokenAdd Class
Handler class for adding new events, tasks, and time blocks to the database.

**Constructor:**
- `TokenAdd(tokenObject)`: Initializes with a Tokens object

**Methods:**

##### addEvent()
Adds a new event to the events database table.

**Returns:** str - Success message

**Raises:** Exception if event already exists

**Database Operations:**
- Creates events table if not exists
- Checks for duplicate events
- Inserts new event record

##### addTask()
Adds a new task to the tasks database table.

**Returns:** str - Success message

**Raises:** Exception if incomplete task already exists

**Database Operations:**
- Creates tasks table if not exists
- Checks for duplicate incomplete tasks
- Inserts new task record

##### addBlock()
Adds a new time block to the blocks database table.

**Returns:** str - Success message

**Database Operations:**
- Creates blocks table if not exists
- Inserts new time block record

### scheduling/eventModifiers/tokenModify.py

#### TokenModify Class
Handler class for modifying existing events and tasks.

**Constructor:**
- `TokenModify(tokenObject)`: Initializes with a Tokens object

**Methods:**
- `modifyEvent()`: Updates event properties (description, times)
- `modifyTask()`: Updates task properties (due date, time, urgency)

### scheduling/eventModifiers/tokenRemove.py

#### TokenRemove Class
Handler class for removing events, tasks, and time blocks.

**Constructor:**
- `TokenRemove(tokenObject)`: Initializes with a Tokens object

**Methods:**
- `removeEvent()`: Deletes events from database
- `removeTask()`: Deletes tasks from database
- `removeBlock()`: Deletes time blocks from database

## Calendar Functions

### scheduling/calendarViews/calendarView.py

#### CalendarView Class
Handles calendar display and formatting functions.

**Static Methods:**

##### viewEvents(timeForecast)
Retrieves and formats events for display.

**Parameters:**
- `timeForecast` (int): Time period in seconds

**Returns:** list - Formatted event data

##### convertListToText(eventList)
Converts event lists to formatted text strings.

**Parameters:**
- `eventList` (list): List of event data

**Returns:** str - Formatted text representation

## Task Scheduling

### scheduling/eventScheduler.py

#### Scheduler Class
Handles automatic task scheduling and event retrieval.

**Static Methods:**

##### scheduleTasks(timeForecast)
Main scheduling function that assigns tasks to available time slots.

**Parameters:**
- `timeForecast` (int): Time period for scheduling in seconds

**Process:**
1. Retrieves tasks and existing events
2. Identifies available time slots
3. Assigns tasks based on priority and urgency
4. Updates database with scheduled tasks

##### _calculatePriorityScore(task)
Calculates priority score for task scheduling.

**Parameters:**
- `task` (tuple): Task data including urgency and due date

**Returns:** float - Calculated priority score

##### giveEvents(timeForecast)
Retrieves events from database for specified time period.

**Parameters:**
- `timeForecast` (int): Time period in seconds

**Returns:** list - Event data

##### _giveTasks()
Retrieves unscheduled tasks from database.

**Returns:** list - Task data sorted by priority

##### _giveBlocks()
Retrieves time blocks from database.

**Returns:** list - Time block data

##### _getSchedulingData(timeForecast)
Combines tasks and events for scheduling analysis.

**Parameters:**
- `timeForecast` (int): Time period in seconds

**Returns:** tuple - (tasks, blocks) for scheduling

##### _findAvailableTimeSlots(blocks)
Identifies available time slots between existing events.

**Parameters:**
- `blocks` (list): List of time blocks sorted chronologically

**Returns:** list - Available time slots with buffers

##### _assignTasksToSlots(tasks, availableTime)
Assigns tasks to available time slots.

**Parameters:**
- `tasks` (list): Tasks sorted by priority
- `availableTime` (list): Available time slots

**Returns:** list - Successfully scheduled tasks

## Messaging Functions

### messaging/sendMessage.py

#### Functions

##### getTextMessageInput(recipient, text)
Creates WhatsApp message payload.

**Parameters:**
- `recipient` (str): Phone number of recipient
- `text` (str): Message text

**Returns:** dict - WhatsApp API message payload

##### sendToUser(data)
Sends message via WhatsApp Business API.

**Parameters:**
- `data` (dict): Message payload

**Returns:** Response from WhatsApp API

##### messageUser(message)
Sends message to default recipient.

**Parameters:**
- `message` (str): Message text to send

### messaging/recieveMessage.py

#### Functions

##### verify(request)
Webhook verification endpoint for Meta API.

**Parameters:**
- `request`: FastAPI request object

**Returns:** Verification token or 403 error

##### receive(request)
Processes incoming WhatsApp messages.

**Parameters:**
- `request`: FastAPI request object

**Returns:** HTTP 200 response

## Utility Functions

### utils/timeUtilitities/timeUtil.py

#### TokenizeToDatetime Class
Parses date/time strings into datetime objects with timezone handling.

**Constructor:**
- `TokenizeToDatetime(timeString)`: Initializes with date/time string

**Methods:**
- `_splitTime(timeString)`: Internal method for parsing time components

**Attributes:**
- `datetimeObj` (datetime): Parsed datetime object with timezone

#### TimeUtility Class
Main time conversion and manipulation class.

**Constructor:**
- `TimeUtility(intoUnix=None, unixTimeUTC=None)`: Initialize with time string or Unix timestamp

**Methods:**
- `updateCurrentTime()`: Updates current time to now
- `convertToUTC()`: Converts local time to UTC Unix timestamp
- `generateTimeDataObj()`: Creates TimeData object from current time

**Attributes:**
- `currentTime` (float): Current Unix timestamp
- `datetimeObj` (TimeData): Structured time data object

#### Functions

##### toSeconds(time)
Converts time string to total seconds.

**Parameters:**
- `time` (str): Time in format "HH:MM" or "HH:MM:SS"

**Returns:** int - Total seconds

##### timeOut(timeString)
Converts time period string to seconds.

**Parameters:**
- `timeString` (str): Time period like "7 D" (days)

**Returns:** int - Total seconds

##### toShortHumanTime(unixTime)
Converts Unix timestamp to readable date.

**Parameters:**
- `unixTime` (int): Unix timestamp

**Returns:** str - Formatted date string

##### toHumanHour(unixTime)
Converts Unix timestamp to readable time.

**Parameters:**
- `unixTime` (int): Unix timestamp

**Returns:** str - Formatted time string

##### deltaToStartOfWeek(currentTime)
Calculates seconds since start of week.

**Parameters:**
- `currentTime` (int): Current Unix timestamp

**Returns:** int - Seconds since Monday 00:00

### utils/timeUtilitities/timeDataClasses.py

#### TimeData Class
Dataclass for structured time information.

**Attributes:**
- `monthNum` (int): Month number (01-12)
- `monthName` (str): Full month name
- `dayOfWeek` (str): Full day name
- `day` (int): Day of month (01-31)
- `hour` (int): Hour (00-23)
- `minute` (int): Minute (00-59)
- `second` (int): Second (00-59)
- `dayNumInWeek` (int): Day number in week (1-7)
- `year` (int): Four-digit year
- `unixTimeUTC` (float): Unix timestamp in UTC
- `timeZone` (str): User's timezone from configuration

#### UnixTimePeriods Class
Constants for common time periods in seconds.

**Attributes:**
- `minute` (int): 60 seconds
- `hour` (int): 3,600 seconds
- `day` (int): 86,400 seconds
- `week` (int): 604,800 seconds

### utils/timeUtilitities/startAndEndBlocks.py

#### TimeStarts Class
Calculates start/end times for various time periods.

**Constructor:**
- `TimeStarts(generationTime=None)`: Initialize with specific time or current time

**Methods:**
- `setToday()`: Calculate today's start/end times
- `setThisWeek()`: Calculate this week's start/end times
- `setDaysOfThisWeek()`: Generate tuple of days in current week
- `setFloatingWeek()`: Calculate floating week from current day
- `setDaysOfFloatingWeek()`: Generate tuple of days in floating week
- `setThisMonth()`: Calculate this month's start/end times
- `setDaysOfMonth()`: Generate tuple of all days in current month

**Attributes:**
- `today` (dict): Start/end times for today
- `thisWeek` (dict): Start/end times for this week
- `daysOfThisWeek` (tuple): Unix timestamps for each day of current week
- `floatingWeek` (dict): Start/end times for floating week
- `daysOfFloatingWeek` (tuple): Unix timestamps for each day of floating week
- `thisMonth` (dict): Start/end times for this month
- `daysOfMonth` (tuple): Unix timestamps for each day of current month

## Calendar Generation Functions

### calendarORGS/calendarViews/calendarCreator/generateCalendar.py

#### sortedEventsObj Class
Dataclass for categorized event lists.

**Attributes:**
- `today` (list): Events occurring today
- `thisWeek` (list): Events occurring this week

#### CalendarCreator Class
Main calendar generation class for web-based calendar views.

**Constructor:**
- `CalendarCreator()`: Initialize with templates and event data

**Methods:**
- `sortEventsDay()`: Sort events into daily and weekly categories
- `createCalendar()`: Generate HTML calendar output using templates

**Attributes:**
- `env` (Environment): Jinja2 template environment
- `weekTemplate` (Template): Loaded week calendar template
- `timeStarts` (TimeStarts): Time period calculation object
- `unsortedEvents` (list): Raw event data from database
- `sortedEvents` (sortedEventsObj): Categorized event data

### utils/dbUtils.py

#### ConnectDB Class
Manages SQLite database connections.

**Constructor:**
- `ConnectDB()`: Initializes database connection and cursor

**Methods:**
- `getDBPath()`: Returns absolute path to calendar.db
- `initConnection()`: Establishes database connection
- `dbCleanup()`: Handles connection cleanup

**Attributes:**
- `conn`: SQLite connection object
- `cursor`: Database cursor object

### utils/jsonUtils.py

#### Functions

##### loadConfig()
Loads application configuration from config.json.

**Returns:** dict - Configuration data including API tokens

## Database Schema

The application uses SQLite with three main tables:

### events table
- `event` (text): Event name/identifier
- `description` (text): Event description
- `unixtimeStart` (integer): Start time as Unix timestamp
- `unixtimeEnd` (integer): End time as Unix timestamp
- `task` (boolean): Whether this is a task (default: False)
- `completed` (boolean): Completion status (default: False)

### tasks table
- `task` (text): Task name/identifier
- `unixtime` (integer): Estimated completion time in seconds
- `urgency` (integer): Urgency level (1-5)
- `scheduled` (boolean): Whether scheduled (default: False)
- `dueDate` (integer): Due date as Unix timestamp
- `completed` (boolean): Completion status (default: False)

### blocks table
- `timeStart` (integer): Block start time as Unix timestamp
- `timeEnd` (integer): Block end time as Unix timestamp

## Error Handling

All modules implement comprehensive error handling:
- Input validation for time formats and command structure
- Database connection error handling
- Exception propagation with meaningful error messages
- Graceful handling of duplicate entries and missing records

## Usage Examples

### Adding an Event
```python
# Command: EVENT ADD "Meeting" 25/12/2023 14:30 25/12/2023 15:30 "Team standup"
tokenizer = CommandTokenizer(command)
factory = TokenFactory(tokenizer.tokenObject)
result = factory.doToken()
```

### Scheduling Tasks
```python
# Command: SCHEDULE 7 D
tokenizer = CommandTokenizer(command)
factory = TokenFactory(tokenizer.tokenObject)
result = factory.doToken()  # Returns formatted calendar with scheduled tasks
```
