from django.contrib import admin
from django.urls import path
from application import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('populate_database',views.populate_database, name='populate_database'),
    path('delete_database',views.delete_database, name='delete_database'),
    path('criar_projeto',views.page_create, name='criar_projeto'),
    path('create',views.create, name='create'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('compare/<int:id>', views.compare, name='compare'),
    path('compare_stock/<int:id>', views.compare_stock, name='compare_stock'),
]
