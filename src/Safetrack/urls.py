from django.conf.urls.defaults import patterns, include, url
from Safetrack.tracker import views, supportFunc
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Safetrack import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Safetrack.views.home', name='home'),
    # url(r'^Safetrack/', include('Safetrack.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.loginView,name="LOGIN"),
    url(r'^logout/', views.logoutView,name="LOGOUT"),
    url(r'^start/', views.startPolling),
    url(r'^employee/', views.renderDataEmployee),
    url(r'^management/', views.renderDataManagement),
    url(r'^supervisor/', views.renderDataSupervisor),
    url(r'^testSend/', views.testSendFromServer),
    url(r'^addDummyData/', views.addDummyDataToDb),
    url(r'^testingFeedback/', views.testFeedback),   

    #ajax calls
    url(r'^addUser.py/', views.addUser),
    url(r'^removeUser.py/', views.removeUser),
    url(r'^getMembers.py/', views.getMembers),
    url(r'^getUsersStatus.py',views.getUsersStatus),
    url(r'^getUsers.py',views.getUsers),
    url(r'^getNewChartData/', views.getNewChartData),
    url(r'^getTemperatureData/', supportFunc.getTemperatureData),
    url(r'^getNoiseData/', supportFunc.getNoiseData),
    url(r'^getHumidityData/', supportFunc.getHumidityData),
    url(r'^getImpactData/', supportFunc.getImpactData),

    url(r'', views.loginView,name="LOGIN"),
)
urlpatterns += staticfiles_urlpatterns()
