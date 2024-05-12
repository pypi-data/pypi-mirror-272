from ntphy.utils.server import Server
from ntphy.utils.calculate import Calculate
from ntphy.utils.messages import Messages

class Output:
    def __init__(self):
        self.server = Server()
        self.calculate = Calculate()
        self.messages = Messages(self)

    def initial_connection(self):

        subscription_list = self.server.subscriptions_list()

        # Calculate the maximum length of each field for even spacing
        max_name_len = self.calculate.name_length(subscription_list)
        max_url_len = self.calculate.url_length(subscription_list)
        max_description_len = self.calculate.description_length(subscription_list)
        separator_length = self.calculate.separator_length(max_name_len, max_url_len, max_description_len)

        # Print the formatted subscription details
        print("\nLISTENING TO SUBSCRIBED TOPICS:\n")
        for i, (name, url, description) in enumerate(subscription_list, start=1):
            url = url.replace('/json', '') # Remove /json to avoid confusion in topic names
            print(f"{i}. {name:<{max_name_len}} || {url:<{max_url_len}} || {description:<{max_description_len}}")
        print("-" * separator_length)

    def message(self, event_type, topic, message, title):
        if title != "N/A":
            print(f'\n[{self.server.subscription_name_from_topic(topic)}]: "{title}"')
        else:
            print(f"\n[{self.server.subscription_name_from_topic(topic)}]")
        # if event_type not in ["message", "open"]:
        #     print(f"Event: {event_type}")
        if message != "N/A":
            print(f"Message: {message}")
        # if message != "N/A":
        #     sections_to_check = ['$_Media', '$_Request', '$_Issue', '$_Comment']
        #     section_found = False

        #     for section in sections_to_check:
        #         section_content = self.messages.filter_section(section, message)
        #         print(f"Section: {section_content}")
        #         if section_content:
        #             print(section_content)
        #             print("-" * 30)
        #             section_found = True

        #     if not section_found:
        #         print(message)
        #         print("-" * 30)

        #     print("\n")
        # else:
        #     print('...')
