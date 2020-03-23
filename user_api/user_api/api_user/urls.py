from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('users', views.UserProfileViewSet)
router.register('services', views.MakeService,basename='Service')
router.register('services_list',views.ListServices,basename='List-Service')
router.register('service_request',views.MakeServiceRequest,basename='Service-Request')
router.register('request_to_provider',views.RequestsToProvider,basename='Request-Provider')
router.register('comments',views.CreateComment,basename='Comments-on-Service')


urlpatterns = [

    path('', include(router.urls)),
    path('login/', views.UserLoginViewSet.as_view()),
    # path('login/',views.UserLoginApiView.as_view()),
    path('logout/',views.UserLogout.as_view()),
    path('update/', views.UserUpdateView.as_view()),
    path('password/',views.APIChangePasswordView.as_view()),
    path('delete/<int:pk>/',views.DeleteUserDetails.as_view()),
    path('comment_view/<int:pk>/', views.ViewComments.as_view(), name="comment_views")

]
