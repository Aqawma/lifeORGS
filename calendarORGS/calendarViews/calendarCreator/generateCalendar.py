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
        try:
            # Ensure parent directory exists
            self.cssDestPath.parent.mkdir(parents=True, exist_ok=True)

            if self.cssDestPath.exists():
                shutil.rmtree(self.cssDestPath)
            shutil.copytree(self.cssTemplatePath, self.cssDestPath)

            # Recreate .gitkeep file to preserve directory structure in version control
            gitkeepPath = self.cssDestPath / ".gitkeep"
            gitkeepPath.touch()
        except FileNotFoundError:
            print("Error: CSS template not found.")
        except Exception as e:
            print(f"Error: {e}")

    def _copyJS(self):
        try:
            self.JSDestPath.parent.mkdir(parents=True, exist_ok=True)

            if self.JSDestPath.exists():
                shutil.rmtree(self.JSDestPath)
            shutil.copytree(self.JSTemplatePath, self.JSDestPath)

            gitkeepPath = self.JSDestPath / ".gitkeep"
            gitkeepPath.touch()
        except FileNotFoundError:
            print("Error: JS template not found.")
        except Exception as e:
            print(f"Error: {e}")

    def createDayCalendar(self):
        """
        Generate HTML content from dayTemplate.html template with today's events.

        Returns:
            str: Rendered HTML content for the day calendar
        """
        # Render the day template with today's events
        outputs = self.dayTemplate.render(
            todayEvents=self.sortedEventsToday,
            eventColors=ColorGenerator().generateColorList(len(self.sortedEventsToday)),
            colorDict=Configs().colorSchemes
        )
        self._copyCSS()
        self._copyJS()
        CalendarView.createEventJson()
        return outputs


# Main execution block - Generate and save calendar HTML
if __name__ == "__main__":
    # Create calendar instance and generate HTML
    calendar = CalendarCreator()
    output = calendar.createDayCalendar()

    # Save generated calendar to index.html
    cal_index_path = Path(getProjRoot()) / "calendarORGS" / "calendarViews" / "calendarSite" / "index.html"

    # Create parent directories if they don't exist
    cal_index_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    cal_index_path.write_text(output)

    print(f"Day calendar generated and saved to: {cal_index_path}")

# Also execute when imported (for backward compatibility)
calendar = CalendarCreator()
output = calendar.createDayCalendar()
cal_index_path = Path(getProjRoot()) / "calendarORGS" / "calendarViews" / "calendarSite" / "index.html"

# Create parent directories if they don't exist
cal_index_path.parent.mkdir(parents=True, exist_ok=True)

# Write the file
cal_index_path.write_text(output)
