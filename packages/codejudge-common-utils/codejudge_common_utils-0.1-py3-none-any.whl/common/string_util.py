import re


class StringUtil:

    @classmethod
    def title_case(cls, string):
        return string.title() if string else string

    @classmethod
    def wrap_single_quote(cls, item):
        return "'" + item + "'"

    @classmethod
    def trim(cls, item):
        return item.strip()

    @classmethod
    def de_emojify(cls, text):
        regrex_pattern = re.compile(pattern="["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            "]+", flags=re.UNICODE)
        return regrex_pattern.sub(r'', text)

    @classmethod
    def replace(cls, text, old_value, new_value):
        return text.replace(old_value, new_value)

    @classmethod
    def is_valid(cls, text):
        return False if (text is None or len(cls.trim(text)) == 0) else True

    @classmethod
    def get_str_from_bytes(cls, input_bytes, encoding='utf-8'):
        return input_bytes.decode(encoding, errors='ignore')

    @classmethod
    def escape_text(cls, text):
        return text.encode('unicode-escape').decode()

    @classmethod
    def get_upper_case(cls, string):
        return string.upper()

    @classmethod
    def convert_complete_string_in_title_case(cls, string):
        words = string.split()
        title_case_words = [cls.title_case(word) for word in words]
        title_case_string = ' '.join(title_case_words)
        return title_case_string


