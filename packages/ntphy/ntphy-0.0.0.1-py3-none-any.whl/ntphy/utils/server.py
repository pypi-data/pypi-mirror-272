# ntphy/utils/server.py

# Standard Imports
import configparser         # Used to parse 'ini' files
from pathlib import Path    # Used to read directory paths

# Information about your ntfy server
class Server:

    # Initialize config files
    def __init__(self):
        self.package_root = Path(__file__).resolve().parents[1]
        self.server_file = self.package_root / 'dev_config' / 'server.ini'
        self.subscriptions_file = self.package_root / 'dev_config' / 'subscriptions.ini'

    # Returns the server address
    def url(self):
        """
        Description:
            Retrieve the server address from the `server.ini` file.

        Returns:
            str: The server address.
        """

        ## INITIALIZE SERVER
        server = configparser.ConfigParser()
        server.read(self.server_file)

        # SERVER ADDRESS
        ntfy_server = server['NTFY'].get('url', '')
        return ntfy_server

    # Returns a list of subscribed topics
    def subscriptions_list(self):
        """
        Description:
            Retrieve subscription information from the `subscriptions` object initialized in `ntfy_client`.

        Returns:
            list: A list of tuples containing the name, URL, and description of each subscription.
        """

        # Initialize subscription list
        subscriptions_info = []

        # Retrieve the server address
        client_server = self.url()

        # Retrieve subscription information from the `subscriptions` object initialized in `ntfy_client`
        client_subscriptions = configparser.ConfigParser()
        client_subscriptions.read(self.subscriptions_file)
        for section in client_subscriptions.sections():
            name = client_subscriptions.get(section, 'name', fallback='N/A')
            topic = client_subscriptions.get(section, 'topic', fallback='N/A')
            description = client_subscriptions.get(section, 'description', fallback='N/A')
            url = f"{client_server}/{topic}/json"
            subscriptions_info.append((name, url, description))

        # Sort subscriptions alphabetically by name
        subscriptions_info.sort(key=lambda x: x[0])

        return subscriptions_info

    def subscription_name_from_topic(self, topic_name):
        """
        Description:
            Retrieve the subscription name from the URL.

        Args:
            url (str): The URL of the subscription.

        Returns:
            str: The subscription name.
        """

        # Retrieve subscription information from the `subscriptions` object initialized in `ntfy_client`
        client_subscriptions = configparser.ConfigParser()
        client_subscriptions.read(self.subscriptions_file)
        for section in client_subscriptions.sections():
            name = client_subscriptions.get(section, 'name', fallback='N/A')
            topic = client_subscriptions.get(section, 'topic', fallback='N/A')
            if topic == topic_name:
                return name

        return None

    # Returns a dictionary of subscribed topics
    def subscriptions_dict(self):
        """
        Description:
            Create a dictionary mapping subscription names to their respective URLs.

        Args:
            subscriptions_info (list): A list of tuples containing the name, URL, and description of each subscription.

        Returns:
            dict: A dictionary mapping subscription names to their respective URLs.
        """

        return {name: url for name, url, _ in self.subscriptions_list()}