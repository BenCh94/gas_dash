from django import template

register = template.Library()


@register.filter(name='percentage')  
def percentage(fraction):  
    try:  
        return "%.2f%%" % (float(fraction) * 100)  
    except ValueError:  
        return ''

@register.filter(name='big_number')
def big_number(big_num):
	if big_num < 1000000:
		return big_num
	elif big_num < 1000000000:
		mil = "%.2f" % (big_num/1000000)
		return str(mil)+" Million"
	else:
		bil = "%.2f" % (big_num/1000000000)
		return str(bil)+" Billion"
