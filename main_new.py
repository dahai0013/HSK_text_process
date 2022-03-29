import argparse
import json
import csv
from datetime import datetime
from datetime import timezone
from dateutil import parser as dtparse
import re


class ParseConversation:
    """ A wrapper class with functions to parse the .json files and convert to .csv
       based on user preferences """

    def __init__(self, file_path=''):

        self.file = open(file_path, 'r', encoding='utf-8')
        self.file_contents = self.file.read()
        self.file.close()
        self.conversations = ''

    def get_conversations(self) -> list:
        """ Sets attribute 'conversations' to the class object """

        json_object = json.loads(self.file_contents)
        self.conversations = json_object.get('conversations', [])

    def sort_messages(self) -> None:
        """ Sorts messages in a conversation from oldest to newest"""

        for conversation in self.conversations:
            message_list = conversation.get('MessageList', [])
            message_list = list(filter(lambda x: x['messagetype'] == 'RichText', message_list))  # filtering out messages that have RichText format

            for message in message_list:  # converting original arrival time to a datetime object

                # some display names are blank so setting it
                if not message.get('displayName', ''):
                    message['displayName'] = conversation['displayName']

                message['originalarrivaltime'] = dtparse.parse(message['originalarrivaltime'])
            conversation['MessageList'] = message_list


    def ignore_non_chinese(self) -> None:
        """ Function to remove non chinese message in case ignore_non_chinese flag is
        set to true"""

        for conversation in self.conversations:
            message_list = conversation.get('MessageList', [])
            new_message_list = []
            for message in message_list:
                message_content = message['content']
                found = re.findall(r'[\u4e00-\u9fff]+',message_content)
                if found:
                   new_message_list.append(message)
            conversation['MessageList'] = new_message_list




    def export_to_csv(self, output_file_path = 'output.csv') -> None:

        """ Function to export the conversations with their respective display names to
        specified output path.
        The default output path is output.json"""

        with open(output_file_path, 'w' ,encoding='utf-8', newline='') as csvfile:
            fieldnames = ['displayName', 'content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for conversation in self.conversations:
                message_list = conversation.get('MessageList', [])
                for message in message_list:
                    dict_row = {'displayName': message['displayName'],
                                'content': message['content']
                                }
                    writer.writerow(dict_row)


# implementing the argument parser
parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input",
                    help="provide the full path of the input file, default is input.json",
                    type=str)
parser.add_argument("-o", "--output",
                    help="provide the full path of the output file, default is output.json",
                    type=str)
parser.add_argument("--ignore_non_chinese",
                    help="Set this to 'True' if you want to ignore non chinese messages",
                    type=bool)

args = parser.parse_args()
if args.input:
    obj = ParseConversation(args.input)
else:
    obj = ParseConversation('input.json')

obj.get_conversations()
obj.sort_messages()

if args.ignore_non_chinese:
    obj.ignore_non_chinese()

if args.output:
    obj.export_to_csv(output_file_path=args.output)
else:
    obj.export_to_csv()


