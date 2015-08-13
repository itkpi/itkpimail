#Source: https://gist.github.com/sivy/1953457

from django import template
import hashlib

register = template.Library()

#
# {{ "some identifier"|md5 }}
# g87g98ht02497hg349ugh3409h34
#
@register.filter(name='md5')
def md5_string(value):
    return hashlib.md5(value.encode()).hexdigest()
