from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('password/change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password/reset/', auth_views.PasswordChangeView.as_view(), name='password_reset'),
    path('password/reset/done/', auth_views.PasswordChangeView.as_view(), name='password_reset_done'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
