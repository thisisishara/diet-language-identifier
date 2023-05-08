import re
from typing import List


class Preprocessor:
    def __init__(
        self,
        remove_emojis: bool = True,
        remove_emails: bool = True,
        remove_invisible_chars: bool = True,
        remove_numbers: bool = True,
        remove_user_mentions: bool = True,
        remove_hashtags: bool = True,
        remove_emoticons: bool = True,
        remove_urls: bool = True,
        remove_dates: bool = True,
        remove_special_chars: bool = True,
        remove_currency: bool = True,
        remove_measurements: bool = True,
        remove_known_words: bool = True,
        known_words: List = None,
    ):
        self.remove_emojis = remove_emojis
        self.remove_emails = remove_emails
        self.remove_invisible_chars = remove_invisible_chars
        self.remove_numbers = remove_numbers
        self.remove_user_mentions = remove_user_mentions
        self.remove_hashtags = remove_hashtags
        self.remove_emoticons = remove_emoticons
        self.remove_urls = remove_urls
        self.remove_dates = remove_dates
        self.remove_currency = remove_currency
        self.remove_measurements = remove_measurements
        self.remove_known_words = remove_known_words
        self.remove_special_chars = remove_special_chars

        self.known_words = [
            "am",
            "pm",
            "usd",
            "lkr",
            "yen",
            "ren",
            "dollars",
            "dollar",
            "cm",
            "centimeters",
            "meters",
            "meter",
            "centimeter",
            "liter",
            "liters",
            "gallons",
            "gallon",
            "km",
            "kilometer",
            "kilometers",
        ]

        if known_words and isinstance(known_words, List):
            self.known_words = list(set(self.known_words + known_words))

    @staticmethod
    def _remove_emojis(text):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"  # other emoticons
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", text)

    @staticmethod
    def _remove_emails(text):
        email_pattern = re.compile(r"[\w.-]+@[\w.-]+\.\w+")
        return email_pattern.sub(r"", text)

    @staticmethod
    def _remove_user_mentions(text):
        user_mention_pattern = re.compile(r"@\w+")
        return user_mention_pattern.sub(r"", text)

    @staticmethod
    def _remove_hashtags(text):
        hashtag_pattern = re.compile(r"#\w+")
        return hashtag_pattern.sub(r"", text)

    @staticmethod
    def _remove_emoticons(text):
        emoticon_pattern = re.compile(r"[:;=]-?[)(/|\\dp]")
        return emoticon_pattern.sub(r"", text)

    @staticmethod
    def _remove_urls(text):
        url_pattern = re.compile(r"http\S+|www\S+")
        return url_pattern.sub(r"", text)

    @staticmethod
    def _remove_dates(text):
        date_pattern = re.compile(r"\d{1,2}[./-]\d{1,2}[./-]\d{2,4}")
        return date_pattern.sub(r"", text)

    @staticmethod
    def _remove_currency(text):
        currency_pattern = re.compile(r"\b[A-Z]{2,4}\b|\b[$€¥£]\b")
        return currency_pattern.sub(r"", text)

    @staticmethod
    def _remove_measurements(text):
        measurements_pattern = re.compile(
            r"\b[\d.]+\s*(cm|mm|m|km|kg|g|l|ml|gal|°C|°F)\b"
        )
        return measurements_pattern.sub(r"", text)

    @staticmethod
    def _remove_numbers(text):
        number_pattern = re.compile(r"\d+")
        return number_pattern.sub(r"", text)

    def _remove_known_words(self, text):
        words_pattern = re.compile(
            r"\b(" + "|".join(self.known_words) + r")\b", flags=re.IGNORECASE
        )
        return words_pattern.sub(r"", text)

    @staticmethod
    def _remove_special_chars(text):
        special_chars_pattern = re.compile(r"[^a-zA-Z0-9\s]+")
        return special_chars_pattern.sub("", text)

    @staticmethod
    def _remove_invisible_chars(text):
        invisible_pattern = re.compile(r"[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]+")
        return invisible_pattern.sub(r"", text)

    def parse(self, text):
        # # lowering the text assists to match
        # # and remove known words easily [optional]
        # text = text.lower()

        if self.remove_emojis:
            text = self._remove_emojis(text)
        if self.remove_emails:
            text = self._remove_emails(text)
        if self.remove_user_mentions:
            text = self._remove_user_mentions(text)
        if self.remove_hashtags:
            text = self._remove_hashtags(text)
        if self.remove_emoticons:
            text = self._remove_emoticons(text)
        if self.remove_urls:
            text = self._remove_urls(text)
        if self.remove_dates:
            text = self._remove_dates(text)
        if self.remove_currency:
            text = self._remove_currency(text)
        if self.remove_measurements:
            text = self._remove_measurements(text)
        if self.remove_numbers:
            text = self._remove_numbers(text)
        if self.remove_known_words:
            text = self._remove_known_words(text)
        if self.remove_special_chars:
            text = self._remove_special_chars(text)
        if self.remove_invisible_chars:
            text = self._remove_invisible_chars(text)

        text = text.strip()
        return text


if __name__ == "__main__":
    import sys

    input_ = "2022/02/02 04.02.2036 👋🏽"

    if len(sys.argv) > 1:
        input_ = sys.argv[1]

    preprocessor = Preprocessor()
    parsed_ = preprocessor.parse(text=input_)
    print(f"original text    : [__START__]{input_}[__END__]")
    print(f"preprocessed text: [__START__]{parsed_}[__END__]")
