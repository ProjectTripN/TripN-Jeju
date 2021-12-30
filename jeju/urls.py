

from django.conf.urls import url, re_path
from django.urls import path, re_path

from jeju import views

urlpatterns = [
    # url(r'test', views.test_option),
    # path(r'test', views_test.test_process),
    # path(r'test_user', views_test.test_user),
    path(r'recommendation', views.recommendation),
    path(r'days', views.days),
    url(r'down_csv',views.down),
    # path(r'save_days', views.save_days_d),
    path(r'save_days', views.save_days),
    # url(r'list/(?P<user_id>\w{0,500})$', views.list_by_user),
    url(r'ddd/(?P<user>\w{0,500})$', views.list_by_user_d),
    url(r'pr_days/(?P<user>\w{0,500})$', views.list_by_user_pr),
    url(r'remove/(?P<pk>\w{0,500})$', views.del_list_by_user),
    path(r'update_dday', views.dday_up),
    path(r'all_recommendation', views.list_all)

]