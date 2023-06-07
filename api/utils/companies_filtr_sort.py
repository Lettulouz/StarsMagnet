from django.db.models import Avg, Subquery, Count, When, Case, Q

from api.models import Opinions, Companies


def companies_sorting_filtring(avg_grade, sort_by, sort_dir, has_grades, query=""):
    avg_ratings = Opinions.objects.values('company_id').annotate(avg_rating=Avg('rating')) \
        .filter(avg_rating__range=(avg_grade, 10)).order_by('-avg_rating').values_list('company_id', flat=True)
    opinions = Opinions.objects.filter(company_id__in=Subquery(avg_ratings.values('company_id')))
    opinions_counted = opinions.values('company_id').annotate(count_rating=Count('company_id')) \
        .order_by('-count_rating').values_list('company_id', flat=True)
    results = Companies.objects.filter(Q(name__icontains=query) & Q(status="accepted"))

    if query is not None or query != "":
        if sort_by == 'alphabetically' and sort_dir == 'ASC':
            results = results.filter(Q(pk__in=avg_ratings)).order_by('name')
        elif sort_by == 'alphabetically' and sort_dir == 'DESC':
            results = Companies.objects.filter(Q(pk__in=avg_ratings)).order_by('-name')
        elif sort_by == 'gradesCount' and sort_dir == 'ASC':
            results = Companies.objects.filter(Q(pk__in=avg_ratings)) \
                .order_by(-Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(opinions_counted)], default=99999))
        elif sort_by == 'gradesCount' and sort_dir == 'DESC':
            results = Companies.objects.filter(Q(pk__in=avg_ratings)) \
                .order_by(Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(opinions_counted)], default=99999))
        elif sort_by == 'gradesLevel' and sort_dir == 'ASC':
            results = Companies.objects.filter((Q(pk__in=avg_ratings) if has_grades else Q())) \
                .order_by(-Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(avg_ratings)], default=99999))
        elif sort_by == 'gradesLevel' and sort_dir == 'DESC':
            results = Companies.objects.filter((Q(pk__in=avg_ratings) if has_grades else Q())) \
                .order_by(Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(avg_ratings)], default=99999))

    return results
