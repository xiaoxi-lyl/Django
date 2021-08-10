from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('',views.index,name='index'),
    # django会将访问域名清除，
    # 所以此时只剩下''匹配的就是空字符串''，
    # django会调用相应的views.index函数
    path('posts/<int:pk>',views.detail,name='detail'),

    # 分类视图对应的路径和函数调用
    path('archives/<int:year>/<int:month>/',views.archive,name='archive'),
    path('categories/<int:pk>',views.category,name='category'),
    path('tags/<int:pk>/',views.tag,name='tag'),

]