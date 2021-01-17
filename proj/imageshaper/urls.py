from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add_img', views.add_img, name='add_img'),
    path('resize_view/<int:img_id>', views.resize_view, name='resize_view'),
    path('do_resize', views.do_resize, name='do_resize')
]
