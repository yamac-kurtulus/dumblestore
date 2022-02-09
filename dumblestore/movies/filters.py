from rest_framework.filters import BaseFilterBackend
from django.db.models.functions import Lower
import logging, sys


class GenreOrderingFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        Orders by genre if genre is selected. It uses an additional field in DB because of performance reasons
        """
        ordering_param = request.query_params.get("ordering")
        if ordering_param == "genres":
            return queryset.order_by(Lower("genre_order_index"))
        if ordering_param == "-genres":
            return queryset.order_by(Lower("genre_order_index")).reverse()
        if ordering_param == "title":
            return queryset.order_by(Lower("title"))
        if ordering_param == "-title":
            return queryset.order_by(Lower("title")).reverse()
        return super().filter_queryset(request, queryset, view)
