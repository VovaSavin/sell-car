from django import template
from advertisement.forms import SendMail

register = template.Library()


@register.inclusion_tag('advertisement/tag/send_form.html')
def get_send_form():
    return {'sendform': SendMail()}
