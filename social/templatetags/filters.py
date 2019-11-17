import logging
import re

from django import template
from django.utils.safestring import mark_safe  # import function

from users.decorators import func_log

register = template.Library()

logger = logging.getLogger(__name__)

'''
https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
'''


@func_log
def generate_link(link):
    logger.debug(link)
    return '<a class="link" href="{}">{}</a>'.format(link, link)


@func_log
def generate_hashtag_link(tag):
    logger.debug(tag)

    # Free to configuree the URL the way adapted your project
    url = "/tags/{}/".format(tag)
    logger.debug(url)

    return '<a class="hashtag" href="{}">#{}</a>'.format(url, tag)


@func_log
@register.filter
def render_content(obj):
    logger.debug(obj)

    text = re.sub(r"#(\w+)", lambda m: generate_hashtag_link(m.group(1)), obj)
    logger.debug(text)

    return mark_safe(re.sub(r"(https?://[^\s]+)",
                            lambda m: generate_link(m.group(1)), text))
    # return re.sub(r"(?P<url>https?://[^\s]+)", lambda m: generate_link(m.group(1)), text)


# @func_log
def generate_links(link):
    logger.debug(link)

    # return mark_safe(re.sub(r"(?Phttps?://[^\s]+)",
    #                         lambda m: generate_link(m.group(1)), link))


# register.filter('render_content', render_content)
