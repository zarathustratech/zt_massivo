from django.urls import path

from . import views

urlpatterns = [
    path('', views.PorfolioListView.as_view(), name='portfolio_list'),
    path('create/', views.CreatePortfolioView.as_view(), name='portfolio_create'),
    path('<int:id>/', views.PortfolioRetrieveView.as_view(), name='portfolio_detail'),
    path('<int:id>/upload', views.UploadSourceFileView.as_view(), name='portfolio_upload'),
    path('<int:id>/mapping', views.MappingUpdateView.as_view(), name='portfolio_mapping'),
    path('<int:id>/file-schema/', views.PortfolioFileSchemaView.as_view(), name='portfolio_file_schema'),
    path('table-schemas/', views.TableSchemasView.as_view(), name='portoflio_table_schema'),
    #     path('', views.IndexView.as_view(), name='index'),
    #     path('payments/', views.PaymentView.as_view(), name='payments'),
    #     path('borrowers/', views.BorrowerView.as_view(), name='borrowers'),
    #     path('loans/', views.LoanView.as_view(), name='loans'),
    #     path('upload/', views.RawPortfolioFileView.as_view(), name='porfolio_upload'),
    #     path('save_column_mapping/', views.ColumnMappingView.as_view(), name='save_column_mapping'),
    # path('portfolio/', views.),
    # path('table_schemas/', views.TableSchemasView.as_view(), name='table_schemas'),
    #     path('dummy_data/', views.DummyData.as_view(), name='table_schemas')
    #     # get_schema_view()
]
