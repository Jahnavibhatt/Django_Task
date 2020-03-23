from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet
from . import permission
from . import serializers
from . import models
from rest_framework import generics, mixins
from rest_framework.generics import UpdateAPIView
from django.shortcuts import get_object_or_404
from .permission import IsServiceProvider, IsConsumer


class UserProfileViewSet(viewsets.ModelViewSet):
    """User profile view"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)

    def create(self, request, *args, **kwargs):
        """Create method for user profile"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "User profile created successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def list(self, request, *args, **kwargs):
        """List method to view all user profiles"""
        queryset = models.UserProfile.objects.all()
        serializer = self.get_serializer(queryset, many=True)

        if serializer.data:
            status_header = {
                'status': status.HTTP_200_OK,
                'message': "List of user profiles received successfully.",
                'data': serializer.data
            }
        else:
            status_header = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "No users found",
                "data": {}
            }
        return Response(status_header)


# class UserLoginApiView(ObtainAuthToken):
#     """User Login view"""
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserLoginViewSet(ObtainAuthToken):
    """User Login view"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        status_header = {
            "status": status.HTTP_200_OK,
            "message": "User Logged In Successfully.",
            "token": token.key,
            "data": serializer.data
        }
        return Response(status_header)


class APIChangePasswordView(UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    model = models.UserProfile  # your user model
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(status=200)

    def put(self, request, *args, **kwargs):
        if request.data['old_password'] == request.data['new_password']:
            response = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'New Password should be different from Old Password',
            }
            return Response(response)
        self.object = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if serializer.is_valid():
        #     if not self.object.check_password(serializer.data.get("old_password")):
        #         return Response(
        #             {"old_password": ["Wrong password"]},
        #             status=400
        #         )
        #     self.object.set_password(serializer.data.get("new_password"))
        #     self.object.save()
        #     return Response("Success", status=200)
        #
        # return Response(serializer.errors, status=400)


class UserLogout(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permission.UpdateOwnProfile,)

    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    # def logout(self, request):
    #     try:
    #         request.user.auth_token.delete()
    #     except (AttributeError, ObjectDoesNotExist):
    #         pass
    #
    #     django_logout(request)
    #     return Response(status=status.HTTP_200_OK)


class UserUpdateView(UpdateAPIView):
    """View for updating user profile"""
    serializer_class = serializers.UserProfileUpdateSerializer
    queryset = models.UserProfile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    model = models.UserProfile  # your user model
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def get(self, request, *args, **kwargs):
    #     return Response(status=200)


class DeleteUserDetails(APIView):
    def get(self, request, pk):
        user = get_object_or_404(models.UserProfile, pk=pk)
        serializer_class = serializers.UserProfileSerializer(user)
        return Response(serializer_class.data)

    def delete(self, request, pk):
        user = get_object_or_404(models.UserProfile, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MakeService(viewsets.ModelViewSet):
    """Provider service view"""
    serializer_class = serializers.ServiceSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsServiceProvider)

    def get_queryset(self):
        return models.Service.objects.filter(service_provider=self.request.user)

    def create(self, request, *args, **kwargs):
        """create service method for provider"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = models.UserProfile.objects.get(id=self.request.user.id)
        serializer.save(service_provider=user)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "Provider service created successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def list(self, request, *args, **kwargs):
        """List method to view all services profiles"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "List of provider services received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def retrieve(self, request, *args, **kwargs):
        """Method to retrive particular service."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "Services received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def update(self, request, *args, **kwargs):
        """Method to update particular service."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "Services Updated successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Method to delete particular service."""
        instance = self.get_object()
        if instance.request.filter(status='accepted').count() == 0:
            self.perform_destroy(instance)
            status_header = {
                'status': status.HTTP_200_OK,
                'message': "Service Deleted Successfully.",
            }
            return Response(status_header)
        else:
            status_header = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "The service is currently accepeted. Hence cannot be deleted.",
            }
            return Response(status_header)

    def perform_destroy(self, instance):
        instance.delete()


class ListServices(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """ViewSet for retrieving services"""
    serializer_class = serializers.ServiceSerializer
    queryset = models.Service.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsConsumer)

    def list(self, request, *args, **kwargs):
        """List method to view all services to consumer"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            'status': status.HTTP_200_OK,
            'message': "List of services received successfully.",
            'data': serializer.data
        }
        return Response(status_header)


class MakeServiceRequest(viewsets.ModelViewSet):
    """User request view"""
    serializer_class = serializers.RequestSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsConsumer)

    def create(self, request, *args, **kwargs):
        """Create method to request services for consumer"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = models.UserProfile.objects.get(id=self.request.user.id)
        service = models.Service.objects.get(id=self.request.POST.get('service_id'))
        serializer.save(consumer=user, service_id=service)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "User request created successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def get_queryset(self):
        return models.RequestService.objects.filter(consumer=self.request.user)

    def list(self, request, *args, **kwargs):
        """List method to view all request to consumer"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        sort_field = self.request.query_params.get('sort_by', None)
        # Enter url like '{{base_url}}/api/consumer/requests?sort_by=status/service_id or -status/-service_id'

        if sort_field is not None:
            if (sort_field == 'status') or (sort_field == 'service_id') or (sort_field == '-status') or (
                    sort_field == '-service_id'):
                serializer = self.get_serializer(queryset.order_by(sort_field), many=True)
            else:
                status_header = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': "Bad sorting request.",
                }
                return Response(status_header)
        else:
            serializer = self.get_serializer(queryset, many=True)

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "List of user requests received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def retrieve(self, request, *args, **kwargs):
        """Method to retrive particular request."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "User request received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def update(self, request, *args, **kwargs):
        """Method to update particular request."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "User request updated successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def destroy(self, request, *args, **kwargs):
        """Method to delete particular request."""
        instance = self.get_object()
        if instance.status != "accepted":
            self.perform_destroy(instance)
            status_header = {
                'status': status.HTTP_200_OK,
                'message': "Request Deleted Successfully.",
            }
            return Response(status_header)
        else:
            status_header = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "The request is currently accepeted. Hence cannot be deleted.",
            }
            return Response(status_header)

        # return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class RequestsToProvider(viewsets.ModelViewSet):
    """List of requests to service provider"""
    serializer_class = serializers.RequestSerializer
    authentication_classes = (TokenAuthentication,)
    queryset = models.RequestService.objects.all()
    permission_classes = (IsAuthenticated, IsServiceProvider)

    def get_queryset(self):
        service_obj = self.request.user.services.filter(service_provider=self.request.user)
        request_to_user = []
        for obj in service_obj:
            if len(obj.request.all()) != 0:
                for i in obj.request.all():
                    request_to_user.append(i)
        return request_to_user

    def list(self, request, *args, **kwargs):
        """List method to view all request to provider"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        status_header = {
            'status': status.HTTP_200_OK,
            'message': "List of requests received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def retrieve(self, request, *args, **kwargs):
        """Method to retrive particular request."""
        instance = models.RequestService.objects.get(id=self.kwargs.get('pk'))
        serializer = self.get_serializer(instance)
        status_header = {
            'status': status.HTTP_200_OK,
            'message': "Requests received successfully.",
            'data': serializer.data
        }
        return Response(status_header)

    def update(self, request, *args, **kwargs):
        """Method to update particular request."""
        instance = models.RequestService.objects.get(id=self.kwargs.get('pk'))
        instance.status = request.data.get("status")
        instance.save()
        if request.data['status'].lower() not in ['accepted', 'rejected', 'pending', 'completed']:
            return Response(
                {'status': status.HTTP_400_BAD_REQUEST,
                 'message': "Status can be only 'accepted', 'rejected', 'pending' or 'completed'."})

        if instance.status.lower() == 'accepted' and request.data['status'].lower() == 'rejected':
            return Response({'status': status.HTTP_400_BAD_REQUEST,
                             'message': "You cannot change status now."})
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


class CreateComment(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                    GenericViewSet):
    """Create comment view"""
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsConsumer)

    def create(self, request, *args, **kwargs):
        """Make comment on request"""
        obj = models.RequestService.objects.get(id=self.request.data['request'])
        if obj.status == 'pending':
            status_header = {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "You are not allow to comment, status is pending!.",
            }
            return Response(status_header)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author=self.request.user)
            status_header = {
                'status': status.HTTP_201_CREATED,
                'message': "User comment created successfully.",
                'data': serializer.data
            }
            return Response(status_header)

    def retrieve(self, request, *args, **kwargs):
        """Method to retrive particular comment."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        status_header = {
            'status': status.HTTP_201_CREATED,
            'message': "Comment recieved successfully.",
            'data': serializer.data
        }
        return Response(status_header)

class ViewComments(APIView):
    """View for list of comments per request"""
    serializer_class = serializers.CommentSerializer

    def get(self, request, pk):
            comments = models.Comment.objects.filter(request=pk)
            data = serializers.CommentSerializer(comments,many=True).data
            status_header = {
                'status': status.HTTP_201_CREATED,
                'message': "Comments recieved successfully.",
                'data': data,
            }
            return Response(status_header)
