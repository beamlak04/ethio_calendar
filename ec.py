import math

days_of_week = ['seg', 'mak', 'reb', 'ham', 'arb', 'kid', 'ehu']
months_of_year = ['mes', 'tik', 'hid', 'tah', 'tir', 'yek', 'meg', 'miy',
                    'gin', 'sen', 'ham', 'neh', 'pag']
month_lengths = {
    '30':[month for month in months_of_year[:-1]],
    '5': months_of_year[-1]
}
                    


class EthioCalendar:


    def __init__(self, date) -> None:
        
        self.day = int(self.dateFormatter(date)[0])
        self.month = int(self.dateFormatter(date)[1])
        self.year = int(self.dateFormatter(date)[2])

        assert 0 < self.day < 31, 'there are only 30 days for the first 12 months. days can only be 1-30'
        assert 0 < self.month < 14, 'there are only 13 months. months can only be 1-13'
        if self.month == 13 :
            if self.year % 4 == 3:
                assert 0 < self.day < 7, 'the last month only has 6 days every 4 years. last month can only be 1-6'
            else:
                assert 0 < self.day < 6, 'there is only 5 days in the last month. last month can only be 1-5'

    def dateFormatter(self,date):
        '''
        formats any date given in a form of dd/mm/yyyy
        to a suitable form
        '''
        if '/' in date:
            formatted_date = date.split('/')
        elif '\\' in date:
            formatted_date = date.split('\\')
        return formatted_date
    

    def _isLeapYear(self):
        """
        returns True if the year is a leap year anf False otherwise
        """
        if (self.year + 1 ) % 4 == 0:
            return True
        return False
    

    def yearStartedOn(self):
        """
        returns start of the year 
        """
        firstDay = days_of_week[((int((5500 + self.year)/4) + self.year + 5500) % 7)]
        return firstDay
    

    def monthStartedOn(self):
        month_firstday_index = days_of_week.index(self.yearStartedOn()) + (self.month-1)*2
        if month_firstday_index > 6:
            month_firstday_index -= 7*(month_firstday_index//7)
        
        month_firstday = days_of_week[month_firstday_index]

        return month_firstday


    def findDay(self):
        reference_day = self.monthStartedOn()
        reference_day_index = days_of_week.index(reference_day)

        the_day = self.day + (reference_day_index - 1) - 7*((self.day + reference_day_index -1 )//7)
        return days_of_week[the_day]


    def printMonthCalenar(self):
        """
        takes a month & year and prints out the calendar of the provided month in a tabular way
        """
        month_length = 30

        if months_of_year[self.month-1] == 'pag':
            if self._isLeapYear():
                month_length = 6
            else:
                month_length = 5

        weekly_brk_pnt = lambda start_of_month: [
            len(days_of_week) - days_of_week.index(start_of_month) + 7*d for d in range(5) 
            if len(days_of_week) - days_of_week.index(start_of_month) + 7*d < 31
        ]      
    
        print('====='*5, months_of_year[self.month-1], '====='*5)
        [print(day, end='\t') for day in days_of_week]
        print('')

        print('\t' * days_of_week.index(self.monthStartedOn()) ,end='')
    
        for ken in range(1, month_length + 1):

            if ken not in weekly_brk_pnt(self.monthStartedOn()):
                print(ken, end='\t')
            else:
                print(ken)

        print()


    def printYearCalendar(self):
        """
        prints the calendar of the provided year
        """     
        weekly_brk_pnt = lambda start_of_month: [
            len(days_of_week) - days_of_week.index(start_of_month) + 7*d for d in range(5) 
            if len(days_of_week) - days_of_week.index(start_of_month) + 7*d < 31
        ] 

        print('******'*5, 'CALENDER OF', self.year, '******'*5)
        
        for month in months_of_year:
            month_length = 30
            if month == 'pag':
                if self._isLeapYear():
                    month_length = 6
                else: 
                    month_length = 5 
             
            month_starts_on = days_of_week.index(self.yearStartedOn()) + months_of_year.index(month)*2
            if month_starts_on > 6:
                month_starts_on -= 7 *(month_starts_on//7)

            print('====='*5, month, '====='*5)
            [print(day, end='\t') for day in days_of_week]
            print('\n' + '\t'* month_starts_on, end='')

            for day in range(1, month_length + 1):
                if day not in weekly_brk_pnt(days_of_week[month_starts_on]):
                    print(day, end='\t')
                else:
                    print(day) 

            print()  


    def __gt__(self, date):
        if self.year > date.year:
            return True
        elif self.year == date.year:
            if (self.month - 1) * 30 + self.day > (date.month - 1) * 30 + date.day:
                return True
            return False
        return False

    
    def __lt__(self, date):
        if self.year < date.year:
            return True
        elif self.year == date.year:
            if (self.month - 1) * 30 + self.day < (date.month - 1) * 30 + date.day:
                return True
            return False
        return False
    def __eq__(self, date):
        if self.year == date.year and (self.month - 1) * 30 + self.day == (date.month - 1) * 30 + date.day:
            return True
        return False


    def __ge__(self, date):
        if self.__gt__(date) or self.__eq__(date):
            return True
        return False


    def __le__(self, date):
        if self.__lt__(date) or self.__eq__(date):
            return True
        return False

    def after(self, day, month=0, year=0):
        nth_day = self.day + (self.month - 1) * 30
        days_to_add = day + month * 30 + (year * 365 + year // 4)
        years = self.year

        days = nth_day + days_to_add
        while days > 365:
            if years % 4 == 3:
                if days > 366:
                    years += 1
                    days -= 366
                else:
                    break                
            else:
                years += 1
                days -= 365
        
        months = math.ceil(days / 30)
        days -= days // 30 * 30

        return days, months, years
        

    def before(self, day, month = 0, year=0):
        nth_day = self.day + (self.month - 1) * 30
        days_to_be_subtracted = day + month * 30 + (year * 365 + year // 4)
        years = self.year

        days = nth_day - days_to_be_subtracted
        while days <= 0:
            years -= 1
            if years % 4 == 3:
                days = 366 - abs(days)
            else:
                days = 365 - abs(days)

        months = math.ceil(days / 30)
        days -= days // 30 * 30
        if days == 0:
            days = 30

        return days, months, years        
        

               