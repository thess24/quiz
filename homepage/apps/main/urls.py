from django.conf.urls import patterns, url, include
from apps.main import views
from settings.common import *
 

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^q/(?P<itemid>.+)/$', views.itempage, name='itempage'),
    url(r'^addquestion/', views.addquestion, name='addquestion'),
    url(r'^addanswer/', views.addanswer, name='addanswer'),
    url(r'^userpage/', views.userpage, name='userpage'),
    url(r'^scoreboard/', views.scoreboard, name='scoreboard'),
    url(r'^ajaxsave/', views.ajaxsave, name='ajaxsave'),
    url(r'^ajaxanswer/', views.ajaxanswer, name='ajaxanswer'),
    url(r'^ajaxgroupsub/', views.ajaxgroupsub, name='ajaxgroupsub'),
    url(r'^saved/', views.saved, name='saved'),
    url(r'^submitted/', views.submitted, name='submitted'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^newprofile/', views.newprofile, name='newprofile'),
    url(r'^deletequestion/', views.deletequestion, name='deletequestion'),
    url(r'^c/(?P<category>.+)/new/', views.categorynew, name='categorynew'),    
    url(r'^c/(?P<category>.+)/top/', views.categorytop, name='categorytop'),    
    url(r'^c/(?P<category>.+)/$', views.category, name='category'),    

    # (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #     {'document_root': MEDIA_ROOT}),

) 
 

#### High Importance

# work on user experience if not logged in
# 8. check to make sure signup works
# 9. better homepage?  hot questions -- top categories -- etc
    # wouldyourather, girls, etc
# more stats on page -- boy/girl
# resize image
# something to see if you answered the question


#  ajax answer submit
    # confirm on answer submission --show box or answers for question
    # redo question form so answers are added there as well with ajax

#  Other stuff
    # get google analytics
    # favicon
    # web url



#### Do Sometime
# backend for data gathering, mining
# titles, stickers for completion of questions -- gamification
