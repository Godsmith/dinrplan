from django import template
from django.utils.html import format_html, mark_safe

register = template.Library()


@register.simple_tag
def star_display(rating, max_stars=5):
    """Render a read-only star display for a 0–5 rating."""
    rating = int(rating) if rating else 0
    stars = ""
    for i in range(1, max_stars + 1):
        cls = "bi-star-fill" if i <= rating else "bi-star"
        stars += f'<i class="bi {cls}" aria-hidden="true"></i>'
    label = f"{rating} out of {max_stars} stars"
    return format_html(
        '<span class="star-display" title="{}" aria-label="{}">{}</span>',
        label,
        label,
        mark_safe(stars),
    )
