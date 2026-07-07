from django import template

register = template.Library()


@register.filter
def genre_name(genre, lang):
    return genre.get_name(lang)


@register.filter
def genre_tagline(genre, lang):
    return genre.get_tagline(lang)
