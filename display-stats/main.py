#!/usr/bin/env python3

import re
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse


def main():
    """
    Main function to read and plot language statistics from a csv file.
    """
    parser = argparse.ArgumentParser(
        description='Plot language statistics from a CSV file')
    parser.add_argument('filename', help='Input CSV file name')
    args = parser.parse_args()

    # Open the csv file and parse its contents
    with open(args.filename) as file:
        rawdata = [parse(line) for line in file]

        # Get a list of all languages found in the csv file
        languages = list_languages(rawdata)

        # Extract the statistics for each language and plot the results
        data = extract_stats(rawdata, languages)
        plot_stats(data)


def parse(line):
    """
    Parse a line of text from the csv file.

    Args:
        line: A string containing data from a single row of the csv file.

    Returns:
        A dictionary containing the parsed data.
    """
    items = line.split(';')
    return {
        'hash': items[0],
        'date': items[1],
        'languages': {re.split(' +', item)[2]: re.split(' +', item)[1] for item in items[2:][:-1]}
    }


def list_languages(rawdata):
    """
    Create a list of all unique languages found in the csv file.

    Args:
        rawdata: A list of dictionaries containing the parsed data.

    Returns:
        A list of strings representing unique languages.
    """
    languages = []
    for line in rawdata:
        for lang in line['languages'].keys():
            if lang not in languages:
                languages.append(lang)
    return languages


def extract_stats(rawdata, languages):
    """
    Extract the statistics for each language found in the csv file.

    Args:
        rawdata: A list of dictionaries containing the parsed data.
        languages: A list of strings representing unique languages.

    Returns:
        A dictionary containing the statistics for each language.
    """
    stats = {
        'x': [],
        'y': {}
    }

    for knownlang in languages:
        stats['y'][knownlang] = []

    for line in rawdata:
        date = datetime.datetime.strptime(line['date'], "%Y-%m-%d %H:%M:%S %z")
        stats['x'].append(date)

        for knownlang in languages:
            if knownlang in line['languages']:
                stats['y'][knownlang].append(int(line['languages'][knownlang]))
            else:
                stats['y'][knownlang].append(0)

    return stats


def plot_stats(data):
    """
    Plot the language statistics.

    Args:
        data: A dictionary containing the statistics for each language.
    """
    fig, ax = plt.subplots()

    ax.stackplot(data['x'], *(data['y'].values()), labels=data['y'].keys())

    ax.legend(loc='upper left')
    ax.set_title('Language statistics')
    ax.set_xlabel('Date')
    ax.set_ylabel('Lines of code')

    plt.gcf().autofmt_xdate()

    plt.show()


if __name__ == '__main__':
    main()
