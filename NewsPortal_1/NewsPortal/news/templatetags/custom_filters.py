from django import template

register = template.Library()


CENSOR = ['редиска', 'петрушка', 'свекла']


@register.filter()
def censor(value):
    text = value.split()
    censored = []
    for i in text:
        if i in CENSOR:
            censored.append(i[0] + '*' * (len(i) - 1))
        else:
            censored.append(i)
    return ' '.join(censored)