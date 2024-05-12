# ntphy/apps/jellyseer/receive.py

class Receive:

    def __init__(self):
        pass

    def parse_topic(self, string):
        start_index = string.find("[") + 1
        end_index = string.find("]:")
        topic_string = string[start_index:end_index]
        return topic_string

    def parse_subject(self, string):
        start_marker = "]: \""
        start_index = string.find(start_marker) + len(start_marker)
        end_index = string.find(' {$_', start_index)
        subject_string = string[start_index:end_index]
        return subject_string

    def parse_event(self, string):
        start_index = string.find("{$_") + len("{$_")
        end_index = string.find("}")
        event_string = string[start_index:end_index]
        return event_string

    def parse_media(self, string):
        media_dict = {}
        start_index = string.find("$_Media") + len("$_Media") + 1
        end_index = string.find("$_Request")
        media_info = string[start_index:end_index].strip().split('\n')
        for info in media_info:
            key, value = info.split(': ')
            media_dict[key.strip()] = value.strip().capitalize()
        return media_dict

    def parse_request(self, string):
        request_dict = {}
        start_index = string.find("$_Request") + len("$_Request") + 1
        end_index = string.find("$_Issue")
        request_info = string[start_index:end_index].strip().split('\n')
        for info in request_info:
            key, value = info.split(': ')
            request_dict[key.strip()] = value.strip()
        return request_dict

    def parse_issue(self, string):
        issue_dict = {}
        start_index = string.find("$_Issue") + len("$_Issue") + 1
        end_index = string.find("$_Comment")
        issue_info = string[start_index:end_index].strip().split('\n')
        for info in issue_info:
            if ': ' in info:  # Check if the line contains ': '
                key, value = info.split(': ', 1)
                issue_dict[key.strip()] = value.strip()
        return issue_dict

    def parse_comment(self, string):
        comment_dict = {}
        start_index = string.find("$_Comment") + len("$_Comment") + 1
        comment_info = string[start_index:].strip().split('\n')
        for info in comment_info:
            if ': ' in info:  # Check if the line contains ': '
                key, value = info.split(': ', 1)
                comment_dict[key.strip()] = value.strip()
        return comment_dict

    def parse_all(self, string):
        topic = self.parse_topic(string)
        subject = self.parse_subject(string)
        event_type = self.parse_event(string)
        media_dict = self.parse_media(string)
        request_dict = self.parse_request(string)
        issue_dict = self.parse_issue(string)
        comment_dict = self.parse_comment(string)
        return topic, subject, event_type, media_dict, request_dict, issue_dict, comment_dict

    def translate_event(self, event:str):
        if 'approved' in event.lower():
            return 'Request Submitted'
        elif 'available' in event.lower():
            return 'Request Fulfilled'

    def print_message(self, message, level):
        parsed_message = self.parse_all(message)
        topic = parsed_message[0]
        subject = parsed_message[1]
        event = self.translate_event(parsed_message[2])
        media = parsed_message[3]
        request = parsed_message[4]
        issue = parsed_message[5]
        comment = parsed_message[6]

        if level == 'admin':
            if event == 'Request Submitted':
                print()
                print(f"{topic} Request:\n")
                print(f"TITLE:          {subject}")
                print(f"TYPE:           {media.get('type', 'Null')}")
                print(f"USER:           {request.get('user', 'Null')}")
                if issue.get('id'):
                    print('-' * 36)
                    print(f"ISSUE ID:       {issue.get('id', 'Null')}")
                    print(f"ISSUE TYPE:     {issue.get('type', 'Null')}")
                    print(f"ISSUE STATUS:   {issue.get('status', 'Null')}")
                    print(f"ISSUE USER:     {issue.get('user', 'Null')}")
                if comment.get('comment') or comment.get('user'):
                    print('-' * 36)
                    print(f"COMMENT:        {comment.get('comment', 'Null')}")
                    print(f"COMMENT USER:   {comment.get('user', 'Null')}")
        if level == 'user':
            pass

message = """
[Jellyseer]: "No Way Up (2024) {$_MEDIA_AUTO_APPROVED}"
Message: Characters from different backgrounds are thrown together when the plane they're travelling on crashes into the Pacific Ocean. A nightmare fight for survival ensues with the air supply running out and dangers creeping in from all sides.

$_Media
type: movie
status: PENDING
4k_status: UNKNOWN

$_Request
id: 392
user: odin

$_Issue
id:
type:
status:
user:

$_Comment
comment:
user:
"""
r = Receive()
r.print_message(message, 'admin')

## TODO
# 0. This shit just prints - I need to be sending this to the admin topic and have that show up on my devices
# 1. Implement user level message
# 2. Factor this into the main program