from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("viewpage/<str:entry>/", views.viewpage, name="viewpage"),
    path("editpage/", views.editpage, name="editpage"),
    path("deletepage/", views.deletepage, name="deletepage"),
    path("savepage/", views.savepage, name="savepage"),
    path("newpage/", views.newpage, name="newpage"),
    path("randompage", views.randompage, name="randompage"),    
    path("searchpage/", views.searchpage, name="searchpage")
]
