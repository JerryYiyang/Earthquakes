# NOTE: You shouldn't change anything in this file.
import datetime
import json
import ssl
import urllib.request


# NOTE: Do not change this function.
def get_json(url):
    """Gets JSON data from the given url, and returns it as a
    dictionary.

    Args:
        url: A string of the url from which to get the JSON data.

    Returns:
        A dictionary with the JSON data.
    """
    ctx = ssl.SSLContext()
    with urllib.request.urlopen(url, context=ctx) as response:
        response_text = response.read().decode('utf-8')

    return json.loads(response_text)


# NOTE: Do not change this function.
def time_to_str(time):
    """Converts the given Unix time stamp to a formatted string.

    Args:
        time: An integer number of seconds since Jan 1, 1970 00:00 UTC

    Returns:
        The time string formatted as YY-MM-DD HH:MM:SS in the local time
        zone.
    """
    return datetime.datetime.fromtimestamp(time).isoformat(
        sep=' ', timespec='seconds')
