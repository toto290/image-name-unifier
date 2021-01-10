from debug_utilities import *
import datetime


def find_date_and_time_in_name(name):
    # Date
    log(name)
    schemes = ['YYYY?MM?DD?hh?mm?ss', 'YYYYMMDD?hhmmss', 'YYYYMMDDhhmmss', 'YYYY?MM?DD?hhmmss',
               'YYYYMMDD?hh?mm?ss', 'YYYY?MM?DD', 'YYYYMMDD']  # sorted by priority

    dates_and_times_found = list()
    # apply every scheme
    for scheme in schemes:
        log('scheme = ' + scheme, style='yellow')
        dtes = None
        # apply scheme on every position in str
        for i in range(0, len(name)-len(scheme)+1):
            # date time elements
            dtes = {'Y': list(), 'M': list(), 'D': list(), 'h': list(), 'm': list(), 's': list()}

            scheme_fits = True
            # compare current char with date time elements
            for j in range(0, len(scheme)):
                for dte in list(dtes.keys()):
                    if scheme[j] == dte:
                        log('comparing letter ' + str(name[i + j]) + ' with dte ' + str(dte))
                        if name[i+j].isnumeric():
                            dtes[dte].append(name[i+j])
                        else:
                            scheme_fits = False
                            log('scheme does not apply', style='red')
                if scheme[j] == '?':
                    log('comparing letter ' + str(name[i + j]) + ' with "?"')
                    if name[i+j].isnumeric():
                        scheme_fits = False
                        log('scheme does not apply', style='red')

                # check elements and convert to string or pop
                for dte in list(dtes.keys()):
                    scheme_fits = scheme_fits and len(dtes[dte]) == scheme.count(dte)
                    if scheme_fits:
                        dtes[dte] = ''.join(dtes[dte])
                    else:
                        dtes[dte] = None

                if not scheme_fits:
                    break
            if not scheme_fits:
                break

        if dtes:
            dates_and_times_found.append(dtes)

        log('scheme applied - possible dates and times:', style='blue')
        log(dtes, style='blue')
    log(dates_and_times_found, style='pink')

            #
            # if scheme_fits and check_if_date_and_times_are_valid(dtes['Y'], dtes['Y'], dtes['Y'], dtes['Y'], dtes['Y'], dtes['Y'], dtes['Y']):
            #     #found_dates.append(FoundDate(Y, M, D, schemes[scheme], len(scheme), i))
            #     log('#############')
            #     log(scheme)
            #     log(i)
            #     log('%s-%s-%s' % (str(Y), str(M), str(D)))


def check_if_date_and_times_are_valid(year, month, day, hour, minute, second, earliest_year=1970):
    valid = True

    if year and valid:  # year
        valid = valid and int(datetime.datetime.now().year) >= int(year) >= earliest_year

    if month and valid:  # month
        valid = valid and 12 > int(month) >= 1

    if day and valid:  # day
        max_days = get_number_of_days_in_month(month, year) if month and year else 31
        valid = valid and max_days >= int(day) > 0

    if hour and valid:  # hour
        valid = valid and 24 > int(hour) >= 0

    if minute and valid:  # minute
        valid = valid and 60 > int(minute) >= 0

    if second and valid:  # second
        valid = valid and 60 > int(second) >= 0

    return valid


def get_number_of_days_in_month(year, month):
    try:
        month = int(month)
        year = int(year)
    except ValueError:
        error('value in month or year could not be converted to integer')
        return False
    if 12 >= month >= 1:
        days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        number_of_days = days_per_month[month - 1]
        if month == 2 and check_if_leap_year(year):
            number_of_days += 1
        return number_of_days
    else:
        return False


def check_if_leap_year(year):
    return int(year) % 4 == 0 and not (int(year) % 100 == 0 and not int(year) % 400 == 0)


if __name__ == "__main__":
    log(find_date_and_time_in_name("2012-10-10"))
    # log(check_if_leap_year(2400))
    # log(get_number_of_days_in_month(2001, "lk"))
