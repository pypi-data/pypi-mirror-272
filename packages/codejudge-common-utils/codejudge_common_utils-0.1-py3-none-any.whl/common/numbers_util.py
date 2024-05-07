from decimal import Decimal


class NumbersUtil:

    @classmethod
    def parse_app_version(cls, version):
        return tuple(map(int, version.split('.')))

    @classmethod
    def normalize(cls, version):
        # Split the version string into a list of integers and strings.
        parts = [int(part) if part.isdigit() else part for part in version.split(".")]
        return parts


    @classmethod
    def convert_decimal_number_in_float(cls, decimal_number):
        if isinstance(decimal_number, Decimal):
            return float(decimal_number)
        return decimal_number
