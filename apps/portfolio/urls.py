from django.urls import path

from apps.portfolio.views import (LoanListAPIView, PortfolioListCreateAPIView,
                                  PortfolioRetrieveAPIView)

urlpatterns = [
    path(
        '',
        PortfolioListCreateAPIView.as_view(),
        name='portfolio-list',
    ),
    path(
        '<str:code>/',
        PortfolioRetrieveAPIView.as_view(),
        name='portfolio-retrieve'
    ),
    path(
        '<str:code>/loans/',
        LoanListAPIView.as_view(),
        name='loan-list',
    ),
]
