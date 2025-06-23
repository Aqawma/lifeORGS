import os

def getDBPath():
    """
    Returns the absolute path to the calendar database file.
    
    This ensures that the database file is always accessed from the correct location,
    regardless of the current working directory.
    
    Returns:
        str: Absolute path to the calendar.db file
    """
    # Get the directory of the current file (dbUtils.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Navigate up to the project root (parent of utils directory)
    project_root = os.path.dirname(current_dir)
    
    # Construct the path to the database file
    db_path = os.path.join(project_root, 'calendar.db')
    
    return db_path