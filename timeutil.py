'''
Created on Jan 10, 2013

@author: bchang
'''
def roundToSeconds(millis):
    millisRem = millis % 1000
    if millisRem >= 500:
        return millis / 1000 + 1
    else:
        return millis / 1000

def millisToHHMMSS(millis):
    seconds = roundToSeconds(millis)
    secondsRem = seconds % 60
    minutes = seconds / 60
    minutesRem = minutes % 60
    hours = minutes / 60
    return hours, minutesRem, secondsRem
