# assumes date is valid
def days_since_0(d):

    # we will add Feb 29 later if it's a leap year
    # "30 days, hath September, April, June, and November.."
    days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    days_in_year = 365

    total_days = 0

    # add whole years, excluding extras from leap years
    total_days += days_in_year * d['year']

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


if __name__ == '__main__':

    # 839 days
    date_a = {'year': 2002, 'month': 2, 'day': 14}
    date_b = {'year': 1999, 'month': 10, 'day': 29}

    print(days_since_0(date_a) - days_since_0(date_b))

    # 1 day
    date_a = {'year': 2002, 'month': 2, 'day': 14}
    date_b = {'year': 2002, 'month': 2, 'day': 13}

    print(days_since_0(date_a) - days_since_0(date_b))

    # 366 days (crosses a leap 400 year)
    date_a = {'year': 2001, 'month': 2, 'day': 28}
    date_b = {'year': 2000, 'month': 2, 'day': 28}

    print(days_since_0(date_a) - days_since_0(date_b))

    # 365 days (crosses a leap 100 year)
    date_a = {'year': 1901, 'month': 2, 'day': 28}
    date_b = {'year': 1900, 'month': 2, 'day': 28}

    print(days_since_0(date_a) - days_since_0(date_b))
    
    # 366 days (crosses a leap 4 year that isn't a leap 100 year)
    date_a = {'year': 1989, 'month': 2, 'day': 28}
    date_b = {'year': 1988, 'month': 2, 'day': 28}

    print(days_since_0(date_a) - days_since_0(date_b))

    # -1 days 
    date_a = {'year': 1882, 'month': 12, 'day': 31}
    date_b = {'year': 1883, 'month': 1, 'day': 1}

    print(days_since_0(date_a) - days_since_0(date_b))

