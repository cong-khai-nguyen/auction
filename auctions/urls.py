from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list", views.create, name="createList"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:item>/", views.item, name="item"),
    path("closed_listing/<int:item>/", views.getItemFromClosed, name ="closed_item"),
    path("closed_listing", views.closed, name="closed_listing"),
    path("comment", views.comment, name="comment"),
    path("category", views.category, name= "category"),
    path("category/<str:category>/", views.getCategory, name="get_category")
]
