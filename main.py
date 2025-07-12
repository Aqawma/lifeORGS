"""
lifeORGS - Life Organization System

Main application entry point for the lifeORGS calendar and task management system.
This module provides the interactive command-line interface that continuously prompts
users for commands and processes them through the command parser.

The application supports:
- Event management (add, delete, modify calendar events)
- Task management (add, delete, modify tasks with scheduling)
- Calendar operations (view events, schedule tasks automatically)
- Time block management (define available time periods for scheduling)

Usage:
    python main.py

The application will start an interactive loop where users can enter commands
following the format: <COMMAND_TYPE> <ACTION> [parameters...]

For detailed command reference, see docs/README.md or docs/API.md
"""
from userInteraction.parsing.tokenFactory import TokenFactory
from userInteraction.parsing.tokenize import CommandTokenizer
from utils.dbUtils import ConnectDB


def main():
    """
    Main application loop that provides the interactive command-line interface.

    Continuously prompts the user for commands, processes them through the
    parseCommand function, and displays the results. The loop runs indefinitely
    until the user terminates the application (Ctrl+C).

    The function handles command input, parsing, and output display in a
    simple and user-friendly manner.
    """
    print("Welcome to lifeORGS - Life Organization System")
    print("Type commands to manage your calendar and tasks.")
    print("For help, see the documentation in the docs/ directory.")
    print("-" * 50)

    while True:
        try:
            # Get user input with a clear prompt
            userInput = input("Enter command: ")

            # Skip empty inputs
            if not userInput.strip():
                continue

            # Parse and execute the command
            tokened = CommandTokenizer(userInput)
            factory = TokenFactory(tokened.tokenObject)
            result = factory.doToken()

            connector = ConnectDB()
            connector.conn.close()

            # Display results - handle both single strings and lists
            if isinstance(result, list):
                for res in result:
                    print(res)
            else:
                print(result)

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\nGoodbye! Thank you for using lifeORGS.")
            break
        except Exception as e:
            # Handle any unexpected errors gracefully
            print(f"An error occurred: {e}")
            print("Please try again or check your command format.")


if __name__ == "__main__":
    main()
