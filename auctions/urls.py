from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("category/", views.categories, name="categories"),
    path("sell/", views.sell, name="sell"),
    path("auction/<int:auction_id>/", views.auction, name="auction"),
    path("category/<str:filter>/", views.filter, name="filter"),
    path("watchlist/", views.watchlist, name="watchlist")
]
