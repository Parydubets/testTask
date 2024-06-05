from rest_framework import routers

from app import views, admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include



router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('home', views.Home.as_view(), name="home"),
    #path('admin/', admin.site.urls),
    path('api/users', views.UserCreateAPI.as_view(), name="user-create"),
    path('api/users/<int:id>', views.UserUpdateAPI.as_view(), name="user-update"),
    path('api/restaurants', views.RestaurantAPI.as_view(), name="restaurant-create"),
    path('api/restaurants/<int:id>', views.RestaurantAPI.as_view(), name='restaurant-update'),
    path('api/menus', views.MenuAPIPublic.as_view(), name="menu-create"),
    path('api/menus/<int:id>', views.MenuAPI.as_view(), name="menu-update"),
    path('api/votes', views.VotesAPI.as_view(), name="votes-show"),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]