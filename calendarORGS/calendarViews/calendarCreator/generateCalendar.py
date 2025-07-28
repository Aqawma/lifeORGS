from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import shutil

from calendarORGS.calendarViews.calendarCreator.calendarView import EventSorter, CalendarView
from utils.colorGenerator import ColorGenerator
from utils.jsonUtils import Configs
from utils.projRoot import getProjRoot


class CalendarCreator:
    def __init__(self):
        """
        Initialize the CalendarCreator with templates and event data.

        Sets up the Jinja2 environment, loads the day calendar template,
        initializes time period calculations, and retrieves event data
        from the database.
        """
        # Set up Jinja2 template environment
        self.root = Path(getProjRoot())

        template_path = (self.root
                         / "calendarORGS" / "calendarViews" / "calendarTemplates")
        self.env = Environment(loader=FileSystemLoader(template_path))
        self.dayTemplate = self.env.get_template('dayTemplate.html')

        self.cssTemplatePath = (self.root
                                / "calendarORGS" / "calendarViews" / "calendarTemplates" / "css")
        self.cssDestPath = (self.root
                            / "calendarORGS" / "calendarViews" / "calendarSite" / "css")

        self.JSTemplatePath = (self.root
                               / "calendarORGS" / "calendarViews" / "calendarTemplates" / "js")
        self.JSDestPath = (self.root
                           / "calendarORGS" / "calendarViews" / "calendarSite" / "js")

        self.sortedEvents = EventSorter()
        self.sortedEventsToday = self.sortedEvents.todayEvents

    def _copyCSS(self):
        """
        Copy CSS template files to the calendar site directory.

        Copies all CSS files from the templates directory to the site directory,
        replacing any existing files. Creates necessary parent directories and
        maintains a .gitkeep file for version control.

        Raises:
            FileNotFoundError: If CSS template directory doesn't exist
            Exception: For other file system errors during copy operation
        """
        try:
            # Ensure parent directory exists for destination
            self.cssDestPath.parent.mkdir(parents=True, exist_ok=True)

            # Remove existing CSS directory if it exists to ensure clean copy
            if self.cssDestPath.exists():
                shutil.rmtree(self.cssDestPath)
            # Copy entire CSS template directory to destination
            shutil.copytree(self.cssTemplatePath, self.cssDestPath)

            # Recreate .gitkeep file to preserve directory structure in version control
            gitkeepPath = self.cssDestPath / ".gitkeep"
            gitkeepPath.touch()
        except FileNotFoundError:
            print("Error: CSS template not found.")
        except Exception as e:
            print(f"Error: {e}")

    def _copyJS(self):
        """
        Copy JavaScript template files to the calendar site directory.

        Copies all JavaScript files from the templates directory to the site directory,
        replacing any existing files. Creates necessary parent directories and
        maintains a .gitkeep file for version control.

        Raises:
            FileNotFoundError: If JavaScript template directory doesn't exist
            Exception: For other file system errors during copy operation
        """
        try:
            # Ensure parent directory exists for destination
            self.JSDestPath.parent.mkdir(parents=True, exist_ok=True)

            # Remove existing JS directory if it exists to ensure clean copy
            if self.JSDestPath.exists():
                shutil.rmtree(self.JSDestPath)
            # Copy entire JavaScript template directory to destination
            shutil.copytree(self.JSTemplatePath, self.JSDestPath)

            # Recreate .gitkeep file to preserve directory structure in version control
            gitkeepPath = self.JSDestPath / ".gitkeep"
            gitkeepPath.touch()
        except FileNotFoundError:
            print("Error: JS template not found.")
        except Exception as e:
            print(f"Error: {e}")

    def createDayCalendar(self):
        """
        Generate HTML content from dayTemplate.html template with today's events.

        Creates a complete day calendar by rendering the Jinja2 template with
        today's events, copying necessary CSS/JS files, and generating JSON data
        for the web interface.

        Returns:
            str: Rendered HTML content for the day calendar
        """
        # Render the day template with today's events and styling data
        outputs = self.dayTemplate.render(
            todayEvents=self.sortedEventsToday,  # Events for today with timing metadata
            eventColors=ColorGenerator().generateColorList(len(self.sortedEventsToday)),  # Color palette for events
            colorDict=Configs().colorSchemes  # Color scheme configuration
        )
        # Copy CSS files from templates to site directory
        self._copyCSS()
        # Copy JavaScript files from templates to site directory
        self._copyJS()
        # Generate JSON data file for web calendar interface
        CalendarView.createEventJson()
        return outputs

    @staticmethod
    def CalendarUpdate():
        calendar = CalendarCreator()
        output = calendar.createDayCalendar()
        cal_index_path = Path(getProjRoot()) / "calendarORGS" / "calendarViews" / "calendarSite" / "index.html"

        # Ensure the destination directory exists
        cal_index_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the generated HTML content to the index file
        cal_index_path.write_text(output)
