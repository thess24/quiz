from django.conf.urls import patterns, url, include
from apps.main import views
from settings.common import *
 

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^q/(?P<itemid>.+)/$', views.itempage, name='itempage'),
    url(r'^addquestion/', views.addquestion, name='addquestion'),
    url(r'^addanswer/', views.addanswer, name='addanswer'),
    url(r'^scoreboard/', views.scoreboard, name='scoreboard'),
    url(r'^ajaxsave/', views.ajaxsave, name='ajaxsave'),
    url(r'^ajaxanswer/', views.ajaxanswer, name='ajaxanswer'),
    url(r'^saved/', views.saved, name='saved'),
    url(r'^submitted/', views.submitted, name='submitted'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^newprofile/', views.newprofile, name='newprofile'),
    url(r'^deletequestion/', views.deletequestion, name='deletequestion'),
    url(r'^c/(?P<category>.+)/new/', views.categorynew, name='categorynew'),    
    url(r'^c/(?P<category>.+)/$', views.category, name='category'),    

    # (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #     {'document_root': MEDIA_ROOT}),

) 
 

#### High Importance

# fix how new is displayed
# 2. get comment voting to work
# work on user experience if not logged in
# 8. check to make sure signup works
# 9. better homepage?  hot questions -- top categories -- etc
    # wouldyourather, girls, etc
# subscribed to categories?




#  ajax answer submit
    # confirm on answer submission --show box or answers for question
    # redo question form so answers are added there as well with ajax

#  Other stuff
    # get google analytics
    # favicon




#### Do Sometime
# backend for data gathering, mining
# titles, stickers for completion of questions -- gamification
