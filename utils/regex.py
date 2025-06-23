import re

def smartSplit(text):
    """
    Splits a string by whitespace while preserving content within quotes.

    Args:
        text (str): The input string to split

    Returns:
        list: List of tokens where quoted content remains as single items

    Examples:
        >>> smartSplit('command "first argument" second "third argument"')
        ['command', 'first argument', 'second', 'third argument']

        >>> smartSplit('simple test "with quotes" and "multiple parts"')
        ['simple', 'test', 'with quotes', 'and', 'multiple parts']
    """
    pattern = r'[^\s"]+|"([^"]*)"'

    # Create the result list combining non-quoted and quoted parts
    result = []
    for item in re.finditer(pattern, text):
        # If the match contains a quoted group, use that
        # Otherwise use the full match
        captured = item.group(1)
        if captured is not None:
            result.append(captured)
        else:
            result.append(item.group(0))

    return result
