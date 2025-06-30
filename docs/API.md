# lifeORGS API Documentation

This document provides detailed information about all functions and modules in the lifeORGS application.

## Table of Contents

- [Command Parsing](#command-parsing)
- [Event Management](#event-management)
- [Calendar Functions](#calendar-functions)
- [Messaging Functions](#messaging-functions)
- [Utility Functions](#utility-functions)

## Command Parsing

### parsing/commandParse.py

#### parseCommand(command)
Main command parser that processes user input and routes commands to appropriate functions.

**Parameters:**
- `command` (str): Command string to parse and execute

**Supported Commands:**
- `EVENT ADD <name> <start_date> <start_time> <end_date> <end_time> "description"`
- `EVENT DELETE <name>`
- `EVENT MODIFY <name> DISC "new_description"`
- `EVENT MODIFY <name> STARTTIME <date> <time>`
- `EVENT MODIFY <name> ENDTIME <date> <time>`
- `EVENT MODIFY <name> STARTEND <start_date> <start_time> <end_date> <end_time>`
- `CALENDAR VIEW <number> D`
- `CALENDAR SCHEDULE`
- `TASK ADD <name> <time> <due_date> <due_time> <urgency>`
- `TASK DELETE <name>`
- `TASK MODIFY <name> DUEDATE <date> <time>`
- `TASK MODIFY <name> TIME <time>`
- `TASK MODIFY <name> URGENCY <level>`
- `BLOCK ADD <day> <start_time> <end_time>`

**Returns:** None

## Event Management

### scheduling/calEvent.py

#### addEvent(event, description, startTime, endTime, task=False)
Adds a new event to the calendar database.

**Parameters:**
- `event` (str): Name of the event
- `description` (str): Description of the event
- `startTime` (str): Start time in format 'DD/MM/YYYY HH:MM'
- `endTime` (str): End time in format 'DD/MM/YYYY HH:MM'
- `task` (bool, optional): Indicates if this is a task event. Defaults to False.

**Returns:** str - Success message or error message if event already exists

#### removeEvent(event)
Removes an event from the calendar database.

**Parameters:**
- `event` (str): Name of the event to remove

**Returns:** None

#### addTask(task, time, urgency, due, scheduled=False)
Adds a new task to the calendar database.

**Parameters:**
- `task` (str): Name of the task to be added
- `time` (str): Execution time in format 'HH:MM' or 'HH:MM:SS'
- `urgency` (int): Urgency level of the task (1-5, where 5 is most urgent)
- `due` (str): Due date and time in format 'DD/MM/YYYY HH:MM'
- `scheduled` (bool, optional): Whether the task has been scheduled. Defaults to False

**Returns:** str - Success message or error message if task already exists

#### removeTask(task)
Removes a task from the calendar database.

**Parameters:**
- `task` (str): Name of the task to remove

**Returns:** None

#### modifyTask(task, time, urgency, due, scheduled=False)
Modifies an existing task in the calendar database.

**Parameters:**
- `task` (str): Name of the task to modify
- `time` (str): New time in format 'HH:MM' or 'HH:MM:SS'
- `urgency` (int): New urgency level
- `due` (str): Due date and time in format 'DD/MM/YYYY HH:MM'
- `scheduled` (bool, optional): Whether the task has been scheduled. Defaults to False

**Returns:** None

#### addTimeBlock(day, timeStart, timeEnd)
Adds a time block to the calendar database for scheduling purposes.

**Parameters:**
- `day` (int): Day of the week (1-7, where 1 is Monday)
- `timeStart` (str): Start time in format 'HH:MM' or 'HH:MM:SS'
- `timeEnd` (str): End time in format 'HH:MM' or 'HH:MM:SS'

**Returns:** None

#### removeTimeBlock(timeStart, timeEnd)
Removes a specific time block from the calendar database.

**Parameters:**
- `timeStart` (int): Start time of the block to remove (in seconds)
- `timeEnd` (int): End time of the block to remove (in seconds)

**Returns:** None

## Calendar Functions

### scheduling/calFuncs.py

#### giveEvents(timeForecast)
Retrieves events from the calendar database within a specified time period.

**Parameters:**
- `timeForecast` (str): Time period to look ahead in format "<number> D"

**Returns:** list - List of events as tuples

#### giveTasks()
Retrieves all unscheduled tasks from the calendar database.

**Returns:** list - List of unscheduled tasks as tuples

#### giveBlocks()
Retrieves all time blocks from the calendar database.

**Returns:** list - List of time blocks as tuples

#### viewEvents(timeForecast)
Formats events into a human-readable list grouped by day.

**Parameters:**
- `timeForecast` (str): Time period to look ahead in format "<number> D"

**Returns:** list - List of formatted event strings

#### scheduleTasks(timeForecast)
Schedules tasks within available time blocks while considering existing events.

**Parameters:**
- `timeForecast` (str): Time period for scheduling in format "<number> D"

**Returns:** tuple - (available_time_slots, scheduled_tasks)

## Messaging Functions

### messaging/sendMessage.py

#### getTextMessageInput(recipient, text)
Creates a JSON-formatted WhatsApp text message payload.

**Parameters:**
- `recipient` (str): WhatsApp ID of the message recipient
- `text` (str): Text content of the message to send

**Returns:** str - JSON-formatted string containing the message payload ready for API submission

#### sendToUser(data)
Sends a WhatsApp message using the Meta WhatsApp Business API.

**Parameters:**
- `data` (str): JSON-formatted message payload (typically from getTextMessageInput)

**Side Effects:**
- Prints status and response information to console
- Prints error information if the request fails

**Note:** Uses SSL verification disabled (verify=False) for development

#### messageUser(message)
Sends a text message to the default recipient configured in the system.

**Parameters:**
- `message` (str): Text content of the message to send

**Note:** Uses RECIPIENT_WAID from config.json as the default recipient

### messaging/recieveMessage.py

#### verify(request)
Webhook verification endpoint for Meta WhatsApp Business API.

**Parameters:**
- `request` (Request): FastAPI request object containing query parameters

**Query Parameters:**
- `hub.mode` (str): Should be "subscribe" for verification
- `hub.verify_token` (str): Verification token that must match configured token
- `hub.challenge` (str): Challenge string to return if verification succeeds

**Returns:** PlainTextResponse - Challenge string if verification succeeds (HTTP 200), or "Forbidden" message if verification fails (HTTP 403)

#### receive(request)
Webhook endpoint for receiving incoming WhatsApp messages.

**Parameters:**
- `request` (Request): FastAPI request object containing the webhook payload

**Returns:** dict - Status response indicating the message was received

**Note:** Currently implements a simple echo bot functionality

## Utility Functions

### utils/timeUtils.py

#### toUnixTime(eventTime)
Converts a date and time string to Unix timestamp.

**Parameters:**
- `eventTime` (str): Date and time in format 'DD/MM/YYYY HH:MM'

**Returns:** float - Unix timestamp

#### toSeconds(time)
Converts a time string in HH:MM or HH:MM:SS format to total seconds.

**Parameters:**
- `time` (str): Time string in format 'HH:MM' or 'HH:MM:SS'

**Returns:** int - Total seconds

#### timeOut(timeString)
Converts a time period string to total seconds.

**Parameters:**
- `timeString` (str): Time period string in format "<number> D" for days

**Returns:** int - Total seconds in the specified time period

#### toShortHumanTime(unixTime)
Converts a Unix timestamp to a human-readable date string.

**Parameters:**
- `unixTime` (float): Unix timestamp

**Returns:** str - Formatted date string

#### toHumanHour(unixTime)
Converts a Unix timestamp to a human-readable time string.

**Parameters:**
- `unixTime` (float): Unix timestamp

**Returns:** str - Formatted time string in 12-hour format

#### deltaToStartOfWeek(currentTime)
Calculates the number of seconds elapsed since the start of the current week.

**Parameters:**
- `currentTime` (float): Unix timestamp

**Returns:** int - Number of seconds elapsed since start of week

### utils/dbUtils.py

#### getDBPath()
Returns the absolute path to the calendar database file.

**Returns:** str - Absolute path to calendar.db file

### utils/regex.py

#### smartSplit(text)
Splits a string by whitespace while preserving content within quotes.

**Parameters:**
- `text` (str): The input string to split

**Returns:** list - List of tokens with quoted content preserved

### utils/jsonUtils.py

#### loadConfig()
Loads the application configuration from config.json file.

**Returns:** dict - Dictionary containing all configuration settings from config.json

**Raises:**
- FileNotFoundError: If config.json is not found in the project root
- json.JSONDecodeError: If config.json contains invalid JSON syntax

**Note:** The config.json file should be located in the project root directory

## Database Schema

### events table
- `event` (TEXT) - Event name
- `description` (TEXT) - Event description
- `unixtimeStart` (INTEGER) - Start time as Unix timestamp
- `unixtimeEnd` (INTEGER) - End time as Unix timestamp
- `task` (BOOLEAN) - Whether this is a task event (default: 0)
- `completed` (BOOLEAN) - Whether the event is completed (default: 0)

### tasks table
- `task` (TEXT) - Task name
- `unixtime` (INTEGER) - Estimated duration in seconds
- `urgency` (INTEGER) - Priority level (1-5)
- `scheduled` (BOOLEAN) - Whether task is scheduled (default: 0)
- `dueDate` (INTEGER) - Due date as Unix timestamp

### blocks table
- `timeStart` (INTEGER) - Block start time in seconds
- `timeEnd` (INTEGER) - Block end time in seconds

## Error Handling

All functions include appropriate error handling for:
- Database connection issues
- Invalid time formats
- Duplicate entries
- Missing parameters
- SQL injection prevention through parameterized queries
