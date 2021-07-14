import csv
import json
import urllib.parse
import boto3


def is_anagram(a, b):
    """
    Returns True if both arguments are anagrams.
    """
    try:
        if sorted(a) == sorted(b):
            return True
        else:
            return False
    except Exception as error:
        print("An error has occured: ", repr(error))


def parse_csv(file):
    """
    Reads csv file and returns a list of one list per row.
    """
    with open(file) as csvfile:
        contents = csv.reader(csvfile, dialect='unix')
        potential_anagrams = []
        for row in contents:
            potential_anagrams.append(row)
        return potential_anagrams


def test_csv(file):
    """
    Tests a given csv file for anagrams.
    Returns a list of boolean values.
    """
    anagram_evaluation = []
    for line in parse_csv(file):
        anagram_evaluation.append(is_anagram(line[0], line[1]))
    return anagram_evaluation


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    s3 = boto3.resource('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'],
                                         encoding='utf-8')
    try:
        csvfile = s3.Object(bucket, filename)
        potential_anagrams = csvfile.get()['Body'].read().decode('utf-8')
        print("contents of file: ", potential_anagrams)
        for line in potential_anagrams.splitlines():
            print(is_anagram(line.split(",")[0], line.split(",")[1]))
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}.'.format(filename, bucket))
        raise e
