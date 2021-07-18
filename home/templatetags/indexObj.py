from datetime import date, datetime
from django import template
register = template.Library()


@register.simple_tag
def my_tag(a, b):
    return a[b]


@register.simple_tag
def filterDate(getDate):
    if getDate == '1900-01-01' or getDate == None or getDate == 'Jan. 1, 1900' or getDate == date(1900, 1, 1):
        return ''
    else:
        return getDate


@register.simple_tag
def filterSth(data, without):
    if not data == without:
        return data
    else:
        return ''


@register.simple_tag
def fivePre(num):
    return int((num*5)/100)
