from django_filters import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = NumberFilter(
        field_name='year',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = '__all__'
