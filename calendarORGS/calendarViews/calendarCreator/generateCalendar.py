from jinja2 import Environment, FileSystemLoader
import os

from calendarORGS.calendarViews.calendarCreator.calendarView import EventSorter
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
        template_path = os.path.join(str(getProjRoot()),
                                     "calendarORGS",
                                     "calendarViews",
                                     "calendarTemplates")
        self.env = Environment(loader=FileSystemLoader(template_path))
        self.dayTemplate = self.env.get_template('day.html')

        self.sortedEvents = EventSorter()
        self.sortedEventsToday = self.sortedEvents.todayEvents

    def createDayCalendar(self):
        """
        Generate HTML content from day.html template with today's events.
        
        Returns:
            str: Rendered HTML content for the day calendar
        """
        # Render the day template with today's events
        print(self.sortedEventsToday)
        outputs = self.dayTemplate.render(
            todayEvents=self.sortedEventsToday
        )
        return outputs


# Main execution block - Generate and save calendar HTML
if __name__ == "__main__":
    # Create calendar instance and generate HTML
    calendar = CalendarCreator()
    output = calendar.createDayCalendar()

    # Save generated calendar to index.html
    calIndex = os.path.join(str(getProjRoot()),
                            "calendarORGS",
                            "calendarViews",
                            "calendarSite",
                            "index.html")
    with open(calIndex, "w") as f:
        f.write(output)

    print(f"Day calendar generated and saved to: {calIndex}")

# Also execute when imported (for backward compatibility)
calendar = CalendarCreator()
output = calendar.createDayCalendar()
calIndex = os.path.join(str(getProjRoot()),
                        "calendarORGS",
                        "calendarViews",
                        "calendarSite",
                        "index.html")
with open(calIndex, "w") as f:
    f.write(output)
