import calendar
import datetime
import dateutil
import pandas
from dateutil.relativedelta import relativedelta

def getDateFromSerialNumber (value, error: ["Ignore", "Raise"] = "Ignore"):
    try:
        dt = pandas.to_datetime (value, unit='D', origin='1899-12-30').to_pydatetime()
        return dt
    except:
        if error.lower() == "ignore":
            return value
        elif error.lower() == "raise":
            raise ValueError("value: '{}' is not compatible, please provide value type: int/float")
def getMonthName (monthNumber: int,abbr: bool=True) ->str:
    """
    It returns month name, if abbr=True then 3 lettered otherwise complete month name.
    monthNumber must be in range 0<monthNumber<13
    monthNumber must be int otherwise TypeError
    :param monthNumber:
    :param abbr:
    :return:
    """
    if not isinstance (monthNumber, int):
        raise TypeError("InvlaidMonthTypeException: Month Number must be of int type, provided '{}' type".format (monthNumber.__class__name__))
    if monthNumber<0 or monthNumber>12:
        raise ValueError("InvalidMonth Exception: month value must be in range 1-12, provided value '{}'".format(monthNumber))
    return calendar.month_abbr[monthNumber] if abbr else calendar.month_name [monthNumber]

def getFormatOfDate (requiredFormat: str, date: datetime.datetime)->str:
    """It returns the date in the given format.
        If format is not valid then it will not throw error and returns only that format."""

    result=date.strftime(requiredFormat)
    return result

def convertToDate (strDate: str, dateFormat: str)->datetime.datetime:
    """
    returns datetime format of equivalent strDate given in specified format
    raise ValueError if strDate and given dateFormat not matched or compatible. raise TypeError if strDate or dateFormat is not of str Type.

    :param strDate:
    :param dateFormat:
    :return:
    """
    if isinstance (dateFormat, str) and isinstance (strDate, str):
        result=datetime.datetime.strptime(strDate, dateFormat)
        return result
    else:
        raise TypeError("'strDate' and 'dateFormat' both must be of str type, provided '{}', '{}' type".format (strDate.__class__.__name__, dateFormat.__class__.__name__))

def getFOM(dateObj: datetime.datetime)->datetime.datetime:
    """
    it returns first day of the given dateObj
    :param dateObj: it is date object
    : return:
    """
    if isinstance (dateObj, (datetime.datetime, datetime.date)):
        result=dateObj.replace(day=1)
        return result
    else:
        raise TypeError("dateObj must be 'datetime.datetime' or 'datetime.date type', provided '{}' type".format(dateObj.__class__.__name__))


def getEOM(dateObj: datetime.datetime)->datetime.datetime:
    """
    It current last date of the month of dateObj
    :param dateObj:
    :return:
    """
    if isinstance (dateObj, (datetime.datetime, datetime.date)):
        firstDateOfMonth=dateObj.replace (day=1)
        addOneMonth= dateutil.relativedelta.relativedelta (months=1)
        nextMonthFirstDate=firstDateOfMonth + addOneMonth
        # nextMonthDate=firstDateOfMonth.replace (month=dateObj.month+1)    1`
        # result=nextMonthDate.replace (day 1) - datetime.timedelta (days=1)
        result=nextMonthFirstDate -datetime.timedelta (days=1)
        return result
    else:
        raise TypeError("dateObj must be 'datetime.datetime' or 'datetime.date type', provided '{}' type".format(dateObj.__class__.__name__))

def getCurrentDate()->datetime.datetime:
    """
    It returns the system's current date and time.
    """
    result = datetime.datetime.now()
    return result

def getQuarterNumber (dt: datetime.datetime)->int:
    """
    It returns the quarter number in which the given date object lies.
    Eg: -1 for -> Jan, Feb, Mar
    2 for -> Apr, May, Jun
    3 for -> Jul, Aug, Sep
    4 for -> Oct, Nov, Dec
    :param
    dt: the datetime object whole quarter number is to be find
    return: int(the quarter number in which the given date object lies.)
    """
    timestamp = pandas.Timestamp(dt)
    result = timestamp.quarter
    return result

def getMonthNumberOfQuarter(dt: datetime.datetime) -> int:

    """
    It returns the month number of quarter :
    Eg : Jan, Apr, Jul, Oct --> 1 (1st month of quarter)
        Feb, May, Aug, Nov --> 2
        Mar, Jun, Sep, Dec --> 3 (3rd month of quarter)

    :param dt: The date of which month number is to be determined.
    :return: int (month number of quarter).
    """
    timestamp = pandas.Timestamp(dt)
    qtrNumber = getQuarterNumber(dt)
    result = timestamp.month - ((qtrNumber - 1) * 3)
    return result

def getFirstDateOfQuarter(year: int, quarter: int, isQuarterClose: bool = False):
    """
    year: year: str( % Y - 4 digit year)
    :param year:
    :param quarter: quarter: qtr must be in [q1,q2,q3,q4] or [Q1, Q2,Q3,Q4]
    :param isQuarterClose:
    :return: datetime.datetime: it return first date of the quarter end month.
    """
    if quarter == 1:
        month = "Jan"
        if isQuarterClose:
            month="Feb"
    elif quarter==2:
        month = "Apr"
    elif quarter==3:
        month = "Jul"
    elif quarter==4:
        month = "Oct"
    else:
        raise ValueError("QuarterValueError: quarter must be in [1,2,3,4], provided: '{}'".format(quarter))
    strDt = "{}-{}-1".format(year, month)
    dt = convertToDate (strDt, "%Y-%b-%d")
    return dt

def getLastDateOfQuarter (year: int, quarter: int):
    if quarter==1:
        month = "Mar"
    elif quarter==2:
        month = "Jun"
    elif quarter==3:
        month = "Sep"
    elif quarter==4:
        month = "Dec"
    else:
        raise ValueError("QuarterValueError : quarter must be in [q1,q2,q3,q4] case-insensitive provied : '{}'".format(quarter))
    strDt= "{}-{}-1".format(year,month)
    dt=convertToDate(strDt,"%Y-%b-%d")
    dt=getEOM(dt)
    return dt


def getDateFromQuarter (year: str, quarter: str):
    """
    :param year: str (%Y- 4 digit year)
    :param quarter: qtr must be in [q1,q2, q3, q4] or [Q1, Q2,Q3, Q4]
    : return: datetime.datetime: it return first date of the quarter end month.
    """
    month = ""
    if quarter.lower()=="q1":
        month = "Mar"
    elif quarter.lower()=="q2":
        month = "Jun"
    elif quarter.lower() == "q3":
        month = "Sep"
    elif quarter.lower()=="q4":
        month = "Dec"
    else:
        raise ValueError("QuarterValueError: quarter must be in [Q1, Q2,Q3, Q4] or [q1,q2, q3,q4], provided: '{}'".format(quarter))
    strDt = year + "-" + month + "-1"
    dt = convertToDate (strDt, "%Y-%b-%d")
    return dt

def getDateAfterQuarter (dt: datetime, numberOfQuarter: int):
    if numberOfQuarter<0:
        refDate=getFirstDateOfQuarter (dt.year, getQuarterNumber (dt))
    elif numberOfQuarter>0:
        refDate = getLastDateOfQuarter(dt.year, getQuarterNumber(dt))
    else:
        return dt
    resultDate=getDateAfter(refDate, 3* numberOfQuarter)
    return resultDate

def getDateAfterDays (dt: datetime, numberOfDays: int)->datetime.datetime:
    result=dt +dateutil.relativedelta.relativedelta (days=numberOfDays)
    return result
def getDateDifferenceMonths (gdt: datetime, ldt: datetime)->int:
    gDt = getEOM(gdt)
    lDt = getEOM (ldt)
    relativeDiff = relativedelta (gDt, lDt)
    nMonths = (relativeDiff.months) + (relativeDiff.years * 12)
    return nMonths

def getDateAfter (dt: datetime.datetime, numberOfMonths: int)->datetime.datetime:
    """
    it returns the date after specified number of month
    :param dt:
    :param numberOfMonths:, if numberOfMonths is negative then it returns dates before specified month
    :return: datetime.datetime
    """
    result=dt - dateutil.relativedelta.relativedelta (months=-numberOfMonths)
    return result

if __name__ == '__main__':
    curD=getCurrentDate()
    d=getDateAfterQuarter (curD, -1)
    print(d)