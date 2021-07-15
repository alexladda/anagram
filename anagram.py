import csv
import json
import urllib.parse
import boto3


def is_anagram(a, b):
    """
    Returns True if both arguments are anagrams.
    Returns False if strings are not anagrams or arguments are not strings.
    """
    try:
        if sorted(a) == sorted(b):
            return True
        else:
            return False
    except Exception as error:
        print("An error has occured: ", repr(error))


def test_pairs(potential_anagrams):
    """
    Expects a list with pairs of potential anagrams.
    Tests those pairs for anagrams.
    Returns a list of boolean values for each pair.
    """
    anagram_evaluation = []
    print(potential_anagrams)
    for pair in potential_anagrams:
        anagram_evaluation.append(is_anagram(pair[0], pair[1]))
    return anagram_evaluation


def parse_csv_file(file):
    """
    Opens a local csv file.
    Returns a list of lists: One item per line, each item with the
    potential anagram pair.

    Intended to be used locally from console.

    Out of scope:
    - validating file
    """
    potential_anagrams = []
    with open(file) as csvfile:
        contents = csv.reader(csvfile, dialect='unix')
        for item in contents:
            potential_anagrams.append(item)
        return potential_anagrams


def parse_csv_string(csv_body):
    """
    Expects the contents of a csv file in one single string.
    Returns a list of lists: One item per line, each item with the
    potential anagram pair.

    Out of scope:
    - validating list
    """
    potential_anagrams = []
    print("csv_body", csv_body)
    for row in csv_body:
        potential_anagrams.append(row)
    return potential_anagrams


def lambda_handler(event, context):
    """
    Triggered on upload of any csv file to the specified bucket.
    Returns a list of boolean values.
    Intended to be used locally from console.
    """

    # logging to console
    print("Received event: " + json.dumps(event, indent=2))

    # initializing s3 resource
    s3 = boto3.resource('s3')

    # retrieving information from event
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8')

    # processing uploaded file
    try:
        csvfile = s3.Object(bucket, filename)
        csv_body = csvfile.get()['Body'].read().decode('utf-8')
        # logging raw contents to console
        print("contents of file: ", csv_body)
        # Logging evaluation results to console.
        for line in csv_body.splitlines():
            print(is_anagram(line.split(",")[0], line.split(",")[1]))

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}.'.format(filename, bucket))
        raise e
