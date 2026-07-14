from django import template
from markdown import markdown

register = template.Library()


@register.filter
def genre_name(genre, lang):
    return genre.get_name(lang)


@register.filter
def genre_tagline(genre, lang):
    return genre.get_tagline(lang)


@register.filter
def genre_description(genre, lang):
    return genre.get_description(lang)


@register.filter
def markdown(text):
    return markdown(text, #extensions=['extra']
    )


@register.filter
def car_name(car, lang):
    return car.get_name(lang)


@register.filter
def car_instructions(car, lang):
    return car.get_instructions(lang)
