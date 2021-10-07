from django.urls import path
from . import views

urlpatterns = [
    path(
        '', views.ListAdv.as_view(), name='advertisement'
    ),
    path(
        'my-advertisement', views.MyAdvertisement.as_view(), name='my-advertisement'
    ),
    path(
        'advertisement-by/<slug:author>/<int:pkuser>', views.UserAdvertisement.as_view(), name='his-advertisement'
    ),
    path(
        '<int:pk>', views.DetailAdv.as_view(), name='detail-advertisement'
    ),
    path(
        'create-advertisement', views.CreateAdv.as_view(), name='create-advertisement'
    ),
    path(
        'update-advertisement/<int:pk>', views.UpdateAdv.as_view(), name='update-advertisement'
    ),
    path(
        'edit/<slug:username>', views.EditUser.as_view(), name='edit-pofile'
    ),
    path(
        'rules', views.rules, name='rules'
    ),
    path(
        'about', views.about, name='about'
    ),
    path(
        'support', views.support, name='support'
    ),
]
