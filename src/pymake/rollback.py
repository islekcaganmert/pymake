import os

from pymake.restore import restore
from pymake.check import check


def read_requirements():
    if 'pyproject.toml' in os.listdir():
        with (open('pyproject.toml', 'r') as f):
            req = f.read().split('dependencies = [')[1].split(']')[0].split(', ')
        r = [i.removeprefix('"').removesuffix('"') for i in req]
    elif 'requirements.txt' in os.listdir():
        with (open('requirements.txt', 'r') as f):
            req = f.read().replace('\n\n', '\n')
        r = req.removeprefix('\n').removesuffix('\n').split('\n')
    else:
        r = []
    while '' in r:
        r.remove('')
    return r


def rollback(**kwargs):
    checkpoints = os.listdir('requirements.old')
    if input('Restore to latest checkpoint? (Y/n): ').lower() != 'n':
        checkpoint = checkpoints[-1]
        year = checkpoint[:4]
        month = checkpoint[4:6]
        day = checkpoint[6:8]
        hour = checkpoint[8:10]
        minute = checkpoint[10:12]
        second = checkpoint[12:14]
    else:
        years, year = [], ''
        for i in checkpoints:
            years.append(i[:4])
        years = list(set(years))
        years.sort()
        print(f'Available years: {", ".join(years)}')
        while year not in years:
            year = input('Year: ')

        months, month = [], ''
        for i in checkpoints:
            if i.startswith(year):
                months.append(i[4:6])
        months = list(set(months))
        months.sort()
        print(f'Available months: {", ".join(months)}')
        while month not in months:
            month = input('Month: ')

        days, day = [], ''
        for i in checkpoints:
            if i.startswith(year+month):
                days.append(i[6:8])
        days = list(set(days))
        days.sort()
        print(f'Available days: {", ".join(days)}')
        while day not in days:
            day = input('Day: ')

        hours, hour = [], ''
        for i in checkpoints:
            if i.startswith(year+month+day):
                hours.append(i[8:10])
        hours = list(set(hours))
        hours.sort()
        print(f'Available hours: {", ".join(hours)}')
        while hour not in hours:
            hour = input('Hour: ')

        minutes, minute = [], ''
        for i in checkpoints:
            if i.startswith(year+month+day+hour):
                minutes.append(i[10:12])
        minutes = list(set(minutes))
        minutes.sort()
        print(f'Available minutes: {", ".join(minutes)}')
        while minute not in minutes:
            minute = input('Minute: ')

        seconds, second = [], ''
        for i in checkpoints:
            if i.startswith(year+month+day+hour+minute):
                seconds.append(i[12:14])
        seconds = list(set(seconds))
        seconds.sort()
        print(f'Available seconds: {", ".join(seconds)}')
        while second not in seconds:
            second = input('Second: ')

        checkpoint = year+month+day+hour+minute+second
    print(f'Rolling back to checkpoint from {month}/{day}/{year} {hour}:{minute}:{second}...')

    req = read_requirements()
    while len(req) > 0:
        for i in range(len(req)):
            try:
                print(f'\rCleaning environment... {len(req)} left     ', end=' ', flush=True)
                os.system(f'pymake uninstall {req.pop(i).split(" ")[0]} > /dev/null')
            except IndexError:
                break
        req = read_requirements()
    print('\rCleaning environment... Done!          ')

    restore(file=f'requirements.old/{checkpoint}')
