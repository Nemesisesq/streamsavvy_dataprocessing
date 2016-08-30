import re


def isTimeString(i):
    if re.match('\d{1,2}:\d{1,2}', i) or re.match('AM|PM', i) or re.match('(P|E|C|M)T', i):
        return True

    return False
