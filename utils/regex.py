import re

def smartSplit(text):
    """
    Splits a string by whitespace while preserving content within quotes, including the quotation marks.

    Args:
        text (str): The input string to split

    Returns:
        list: List of tokens where quoted content remains as single items with quotation marks preserved

    Examples:
        >>> smartSplit('command "first argument" second "third argument"')
        ['command', '"first argument"', 'second', '"third argument"']

        >>> smartSplit('simple test "with quotes" and "multiple parts"')
        ['simple', 'test', '"with quotes"', 'and', '"multiple parts"']
    """
    pattern = r'[^\s"]+|"([^"]*)"'

    # Create the result list combining non-quoted and quoted parts
    result = []
    for item in re.finditer(pattern, text):
        # Always use the full match to preserve quotation marks
        result.append(item.group(0))

    return result
