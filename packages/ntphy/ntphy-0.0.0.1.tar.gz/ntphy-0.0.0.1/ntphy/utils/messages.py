# ntphy/utils/messages.py

# Standard Imports
import json
import re

# External Imports
import requests

# Messages from the ntfy server
class Messages:

    # Initialize the output object
    def __init__(self, output):
        self.output = output

    def filter_section(self, section_name, message):
        """
        Filters out sections from a message, ignoring empty sections.

        Args:
            section_name (str): The name of the section (without the '$_' prefix).
            message (str): The message containing the section.

        Returns:
            str: The extracted section if it is non-empty, otherwise None.
        """

        print(f"Section Name: {section_name}")
        print(f"Message: {message}")

        # # Adjust the section name to include the `$_` prefix.
        # section_prefix = f"$_{section_name}"

        # # Match the section prefix followed by content up to the next `$_` or end of the message.
        # pattern = rf"{re.escape(section_prefix)}(.*?)(?=\n\n|\n\$_|\Z)"
        # match = re.search(pattern, message, re.DOTALL)
        # if not match:
        #     return None

        # # Extract the content of the section, filtering out empty lines or lines without values after the colon.
        # section_content = match.group(1)
        # non_empty_lines = [line for line in section_content.splitlines() if line.strip() and ':' in line and line.split(':', 1)[1].strip()]

        # # Return the formatted section if it contains non-empty lines; otherwise, return None.
        # if non_empty_lines:
        #     return f"{section_prefix}:\n" + "\n".join(non_empty_lines)
        # else:
        #     return None

    def filter_message(self, name, url):
        first_message_skipped = False

        resp = requests.get(url, stream=True)
        for line in resp.iter_lines():
            if line:
                event_data = json.loads(line)

                # Skip 'keepalive' events
                if event_data.get("event") == "keepalive":
                    continue

                # Ensure the initial message is skipped
                if not first_message_skipped:
                    first_message_skipped = True
                    continue

                # Retrieve relevant data
                topic = event_data.get("topic", "N/A")
                message = event_data.get("message", "N/A")
                title = event_data.get("title", "N/A")
                event_type = event_data.get("event", "N/A")

                self.output.message(event_type, topic, message, title)