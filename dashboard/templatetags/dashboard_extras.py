from django import template

register = template.Library()


@register.filter(name='percentage')  
def percentage(fraction):  
    try:  
        return "%.2f%%" % (float(fraction) * 100)  
    except ValueError:  
        return ''
