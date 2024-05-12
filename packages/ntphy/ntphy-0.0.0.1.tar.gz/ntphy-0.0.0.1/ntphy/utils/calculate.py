class Calculate():
    def __init__(self):
        pass

    def name_length(self, list):
        return max(len(name) for name, _, _ in list)

    def url_length(self, list):
        return max(len(url.replace('/json', '')) for _, url, _ in list)

    def description_length(self, list):
        return max(len(description) for _, _, description in list)

    def separator_length(self, max_name_len, max_url_len, max_description_len):
        return (
            max_name_len + 2            # Name field length with extra spaces
            + 3                         # Space for the first separator " || "
            + max_url_len + 2           # URL field length with extra spaces
            + 3                         # Space for the second separator " || "
            + max_description_len + 1   # Description field length with extra spaces
        )