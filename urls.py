from django.conf.urls.defaults import patterns, include, url
from Safetrack.tracker import views  

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
    url(r'^login/', views.loginView ),
    url(r'^logout/', views.loginView ),
    url(r'^test/', views.hello_world ),
    url(r'^start/', views.startPolling ),
    url(r'^employee/', views.renderDataEmployee ),
    
    url(r'^testSend/', views.testSendFromServer ),
    url(r'^addDummyData/', views.addDummyDataToDb ),
    
)