from django.urls import include, path
from rest_framework import routers

from testTask.quickstart import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include




router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]