from django import forms
from django.utils.safestring import mark_safe

from .models import Meal


class StarRatingWidget(forms.RadioSelect):
    """Renders a 0–5 star rating as clickable Bootstrap Icons stars."""

    def __init__(self, *args, **kwargs):
        choices = [(i, i) for i in range(6)]  # 0–5
        super().__init__(choices=choices, *args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        current = int(value) if value not in (None, "", "None") else 0
        # Stars rendered 5→1 (flex-direction: row-reverse shows them 1→5 visually).
        # The CSS sibling combinator (~) then lights up all stars with lower values.
        html = '<div class="star-rating" role="radiogroup" aria-label="Rating">'
        for i in range(5, 0, -1):
            checked = "checked" if i == current else ""
            label_title = f"{i} star{'s' if i != 1 else ''}"
            html += (
                f'<input type="radio" class="star-rating__input visually-hidden" '
                f'name="{name}" id="{name}_{i}" value="{i}" {checked}>'
                f'<label class="star-rating__label" for="{name}_{i}" title="{label_title}">'
                f'<i class="bi bi-star-fill" aria-hidden="true"></i>'
                f"</label>"
            )
        # The "0 stars / clear" option — a small ✕ after the stars
        checked_zero = "checked" if current == 0 else ""
        html += (
            f'<input type="radio" class="star-rating__input visually-hidden" '
            f'name="{name}" id="{name}_0" value="0" {checked_zero}>'
            f'<label class="star-rating__label star-rating__clear" for="{name}_0" title="Clear rating">'
            f'<i class="bi bi-x-circle" aria-hidden="true"></i>'
            f"</label>"
        )
        html += "</div>"
        return mark_safe(html)


class MealForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=0,
        max_value=5,
        initial=0,
        widget=StarRatingWidget(),
    )

    class Meta:
        model = Meal
        fields = [
            "name",
            "source",
            "persons",
            "time",
            "ingredients",
            "steps",
            "categories",
            "rating",
        ]


class UploadFileForm(forms.Form):
    meals = forms.FileField()
    days = forms.FileField()
