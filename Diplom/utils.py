from dateutil import parser


def parse_date(date):
    return parser.parse(date).date()


def print_date(date):
    if date is not None:
        year = str(date.year)
        month = str(date.month).rjust(2,'0')
        day = str(date.day).rjust(2,'0')
        return '.'.join([day, month, year])
    else:
        return None
