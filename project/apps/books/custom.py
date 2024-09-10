from django.template.defaulttags import register


# Define range for django jinja template
@register.filter(name='star_range')
def star_range(value):
    return range(1, value + 1)

@register.filter
def get_type(value):
    """
    Return variable type name.
    Usage: {{ value|get_type }}
    """
    return type(value).__name__

@register.filter
def cint(value):
    return int(value)

def average_rating(self):
    ratings = self.ratings.all()
    if ratings:
        return sum(rating.rating for rating in ratings) / ratings.count()
    return 0