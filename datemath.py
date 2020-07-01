from pytest import raises

def days_since_ce(d):

    # we will add Feb 29 later if it's a leap year
    # "30 days, hath September, April, June, and November.."
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_in_year = 365


    if d['year'] < 1:
        raise ValueError("Year must be at least 1")

    if d['month'] < 1 or d['month'] > 12:
        raise ValueError("Month must be 1-12")

    # rewrite this so Feb 29 in a leap year isn't caught
    if d['month'] == 2 and d['day'] == 29:
        if not (
            d['year'] % 4 == 0 and (
                d['year'] % 100 != 0 or\
                d['year'] % 400 == 0
            )
        ):
            raise ValueError("Feb 29 only allowed in leap year")
           
    else:
        if d['day'] < 1 or d['day'] > days_in_month[d['month']]:
            raise ValueError(
                    "Day {} invalid for month {}".format(d['day'], d['month'])
            )

    total_days = 0

    # add whole years, excluding extras from leap years
    # start at year 1 (1 AD)
    total_days += days_in_year * (d['year'] - 1)

    # add extras from leap years
    # don't count the target year if we haven't reached Feb 29
    if d['month'] == 1 or (d['month'] == 2 and d['day'] < 29):
        leap_year_factor = d['year'] - 1
    else:
        leap_year_factor = d['year']

    leap_4_years = int(leap_year_factor / 4)
    leap_100_years = int(leap_year_factor / 100)
    leap_400_years = int(leap_year_factor / 400)

    total_days += (leap_4_years - leap_100_years + leap_400_years)

    # how many days from the start of the year to the target month/date?
    for cur_month in range(1, 13):
        if cur_month < d['month']:
            total_days += days_in_month[cur_month]
        elif cur_month == d['month']:
            total_days += d['day']

    return total_days


def test_date_math():
    
    # 839 days
    date_a = {'year': 2002, 'month': 2, 'day': 14}
    date_b = {'year': 1999, 'month': 10, 'day': 29}

    assert (days_since_ce(date_a) - days_since_ce(date_b)) == 839

    # 1 day
    date_a = {'year': 2002, 'month': 2, 'day': 14}
    date_b = {'year': 2002, 'month': 2, 'day': 13}

    assert (days_since_ce(date_a) - days_since_ce(date_b)) == 1

    # 366 days (crosses a leap 400 year)
    date_a = {'year': 2001, 'month': 2, 'day': 28}
    date_b = {'year': 2000, 'month': 2, 'day': 28}

    assert (days_since_ce(date_a) - days_since_ce(date_b)) == 366

    # 365 days (crosses a leap 100 year)
    date_a = {'year': 1901, 'month': 2, 'day': 28}
    date_b = {'year': 1900, 'month': 2, 'day': 28}

    assert (days_since_ce(date_a) - days_since_ce(date_b)) == 365
    
    # 366 days (crosses a leap 4 year that isn't a leap 100 year)
    date_a = {'year': 1989, 'month': 2, 'day': 28}
    date_b = {'year': 1988, 'month': 2, 'day': 28}

    assert (days_since_ce(date_a) - days_since_ce(date_b)) == 366

    # -1 days 
    date_a = {'year': 1882, 'month': 12, 'day': 31}
    date_b = {'year': 1883, 'month': 1, 'day': 1}

    assert (days_since_ce(date_a) - days_since_ce(date_b)) == -1


def test_date_validity():

    with raises(ValueError):

        # invalid (year < 1)
        days_since_ce({'year': 0000, 'month': 1, 'day': 23})

    with raises(ValueError):

        # invalid (30 days in April)
        days_since_ce({'year': 1900, 'month': 4, 'day': 31})

    with raises(ValueError):

        # invalid (Feb 29 in a non-leap year)
        days_since_ce({'year': 1900, 'month': 2, 'day': 29})

    with raises(ValueError):

        # invalid (Feb 29 in a non-leap year)
        days_since_ce({'year': 2003, 'month': 2, 'day': 29})

    with raises(ValueError):

        # invalid (Jan 32)
        days_since_ce({'year': 1778, 'month': 1, 'day': 32})

    # Feb 29 in a leap year
    days_since_ce({'year': 2000, 'month': 2, 'day': 29})
