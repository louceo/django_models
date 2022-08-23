from django import template

register = template.Library()


@register.filter()
def censor(text):
    bl = ['famous', 'scene', 'drug', 'drugs', 'some', 'texture', 'injected']
    check = text.lower().split(' ')
    text = text.split(' ')
    for i in range(len(check)):
        asteriks = '*' * (len(check[i])-1)
        if check[i][-1] in '.,!?:;':
            if check[i][:len(check[i])-1] in bl:
                text[i] = text[i][:1] + asteriks
        else: 
            if check[i] in bl:
                text[i] = text[i][:1] + asteriks
    text = ' '.join(text)
    return f'{text}'