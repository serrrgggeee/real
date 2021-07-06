from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination,
	)


class LimitOffsetPagination(LimitOffsetPagination):
	default_limit = 2
	max_limit = 10


class PageNumberPagination(PageNumberPagination):
	page_size = 1
		