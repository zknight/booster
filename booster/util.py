import datetime
import re

DEBUG = False
if DEBUG:
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    def dump(s):
        pp.pprint(s)
else:
    def dump(s):
        pass

#####

M_DATE_RE = re.compile(r"""^(?P<m>[01]?\d)[-/.| ]
                            (?P<d>[0123]?\d)[-/.-| ]
                            (?P<y>2?0?\d\d)$""", re.X)
Y_DATE_RE = re.compile(r"""^(?P<y>20\d\d)[-/.| ]
                            (?P<m>[01]\d)[-/.| ]
                            (?P<d>[0123]\d)$""", re.X)
def parse_date(datestr):
# mm/dd/yy, mm-dd-yy, mm.dd.yy
# mm/dd/yyyy
# yyyy/mm/dd
    global M_DATE_RE, Y_DATE_RE
    result = M_DATE_RE.match(datestr)
    if not result:
        result = Y_DATE_RE.match(datestr)
    if not result:
        return None

    d_dict = result.groupdict()
    dump(d_dict)
    return datetime.date(
            int(d_dict['y']), 
            int(d_dict['m']), 
            int(d_dict['d']))


NORM_RE = re.compile(r"""^(?P<H>[012]?\d)
                         (?:
                            (?:[:](?P<M>[012345]\d)
                                (?:[:](?P<S>[012345]\d))?
                            )?
                         )?\s*(?P<P>[aApP][mM]?)?$""", re.X)
MIL_RE = re.compile(r"^(?P<H>[012]\d)(?P<M>[012345]\d)$")

def parse_time(timestr):
# military: 0000-2359
# /(dd)(dd)/
# 24-hour: 00:00:00 - 23:59:59
# /(\d\d?)((:(\d\d))?(:(\d\d))?)?/
# 12-hour: 12:00:00 AM|am|a|A - 11:59:59 PM|pm|p|P
    global NORM_RE
    global MIL_RE

    result = MIL_RE.match(timestr)
    if not result:
        result = NORM_RE.match(timestr)
  
    hour = 0
    minute = 0
    second = 0
    period = False
    hour24 = True

    if result:
        t_dict = result.groupdict()
        if "H" in t_dict:
            hour = int(t_dict["H"])
        if "M" in t_dict and t_dict["M"]:
            minute = int(t_dict["M"])
        if "S" in t_dict and t_dict["S"]:
            second = int(t_dict["S"])
        if "P" in t_dict and t_dict["P"]:
            hour24 = False
            period = "p" in t_dict["P"].lower()
    
        dump(t_dict)
        dump(hour24)
    else:
        return None

# 0a -> None
# 0p -> None
# 12a -> 0
# 1a -> 1
# ...
# 11a -> 11
# 12p -> 12
# 1p -> 13
# 2p -> 14
# ...
# 11p -> 23

    if hour24:
        if hour > 23:
            return None
    else:
        if hour == 0 or hour > 12:
            return None

        if period:
            if hour < 12:
                hour += 12
        elif hour == 12:
            hour = 0

    return datetime.time(hour, minute, second)

if __name__ == "__main__":
    import unittest
    class ParseTimeTest(unittest.TestCase):
        def setUp(self):
            self.mil = [
                    ["0000", datetime.time(0, 0) ],
                    ["0010", datetime.time(0, 10) ],
                    ["1359", datetime.time(13, 59) ],
                    ["2401", None ],
                    ["132", None ],
                    ["3323", None ],
                    ["12345", None ],
                    ]
            self.norm = [
                    ["12p", datetime.time(12, 0) ],
                    ["12pm", datetime.time(12, 0) ],
                    ["12A", datetime.time(0, 0) ],
                    ["13:00", datetime.time(13, 0) ],
                    ["13:01AM", None ],
                    ["1:23pM", datetime.time(13, 23) ],
                    ["43:43:32", None],
                    ["8:54  PM", datetime.time(20, 54) ],
                    ]

        def test_mil(self):
            print
            for case in self.mil:
                result = parse_time(case[0])
                self.assertEqual(result, case[1])

        def test_norm(self):
            print
            for case in self.norm:
                result = parse_time(case[0])
                self.assertEqual(result, case[1])
                 
    unittest.main(verbosity=4)
