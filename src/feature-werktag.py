import datetime

def is_werktag(day, month, year):
    # Create a datetime object for the given date
    date = datetime.date(year, month, day)
    
   
    return date.weekday() != 6

print(is_werktag(12,2,2022))