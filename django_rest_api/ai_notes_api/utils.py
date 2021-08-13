HOURS_MINUTES_DELIMITER = ':'
MORNING_WORDS = ['утра']
NIGHT_WORDS = ['ночи']
DAY_WORDS = ['дня']
EVENING_WORDS = ['вечера']
DAY_MONTH_DELIMITER = '.'
JAN = 'января'
FEB = 'февраля'
MAR = 'марта'
APR = 'апреля'
MAY = 'мая'
JUN = 'июня'
JUL = 'июля'
AUG = 'августа'
SEP = 'сентября'
OCT = 'октября'
NOV = 'ноября'
DEC = 'декабря'
MONTHS = [JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC]
MONTHS_TO_NUMBERS = {JAN: 1, FEB: 2, MAR: 3, APR: 4, MAY: 5, JUN: 6,
                     JUL: 7, AUG: 8, SEP: 9, OCT: 10, NOV: 11, DEC: 12}
MONTHS_NUMBERS_TO_MAX_DAYS = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


class DateTimeExtractor:
    extracted_times = []
    extracted_dates = []

    def __init__(self, input_sentence):
        self.input_sentence = input_sentence
        self.extract_times()
        self.extract_dates()

    def check_and_add_time(self, time_to_check):
        hours_minutes = time_to_check.split(HOURS_MINUTES_DELIMITER)
        if len(hours_minutes) == 2:
            hours = hours_minutes[0]
            minutes = hours_minutes[1]
            if hours.isnumeric() and minutes.isnumeric() and 1 <= len(hours) <= 2 and len(minutes) == 2 and \
                    0 <= int(hours) < 24 and 0 <= int(minutes) < 60:
                self.extracted_times.append(hours + HOURS_MINUTES_DELIMITER + minutes)

    def extract_times(self):
        last_number = None
        for token in self.input_sentence.split():
            if token.isnumeric():
                last_number = token
            elif HOURS_MINUTES_DELIMITER in token:
                self.check_and_add_time(token)
            elif last_number and token in (NIGHT_WORDS + MORNING_WORDS):
                self.check_and_add_time(last_number + HOURS_MINUTES_DELIMITER + '00')
            elif last_number and token in (DAY_WORDS + EVENING_WORDS):
                self.check_and_add_time(str(int(last_number) + 12) + HOURS_MINUTES_DELIMITER + '00')

    def check_and_add_date(self, date_to_add):
        if DAY_MONTH_DELIMITER in date_to_add:
            day_month = date_to_add.split(DAY_MONTH_DELIMITER)
            if len(day_month) == 2:
                day = day_month[0]
                month = day_month[1]
                if day.isnumeric() and month.isnumeric() and 1 <= len(day) <= 2 and \
                        1 <= int(month) <= 12 and 1 <= int(day) <= MONTHS_NUMBERS_TO_MAX_DAYS[int(month)]:
                    self.extracted_dates.append(date_to_add)

    def extract_dates(self):
        last_number = None
        for token in self.input_sentence.split():
            if token.isnumeric():
                last_number = token
            elif last_number and token in MONTHS:
                self.check_and_add_date(last_number + DAY_MONTH_DELIMITER + str(MONTHS_TO_NUMBERS[token]))

    def __str__(self):
        result = f'{self.input_sentence} /'
        if len(self.extracted_times) + len(self.extracted_dates) == 0:
            result += ' -'
        else:
            for time_ in self.extracted_times:
                result += f' {time_}'
            for date_ in self.extracted_dates:
                result += f' {date_}'
        return result
