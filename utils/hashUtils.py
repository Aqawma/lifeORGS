import hashlib
import random
from datetime import datetime

def createHashID():
    """
    Generates a unique hash ID using current timestamp and a random number.

    The function creates a SHA-256 hash by combining the current Unix timestamp
    and a random integer between 1 and 1,000,000,000, providing a high level of
    uniqueness for each generated ID.

    Returns:
        str: A 64-character hexadecimal string representing the SHA-256 hash

    Example:
        >>> createHashID()
        # Returns a string like "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4"

    Note:
        This function is useful for creating unique identifiers for database entries,
        file names, or any other application requiring unique IDs.
    """
    currentTime = datetime.now().timestamp()
    random.randint(1, 1000000000)
    hashID = hashlib.sha256(str(currentTime).encode('utf-8') + str(random.randint(1, 1000000000)).encode('utf-8')).hexdigest()
    return hashID
