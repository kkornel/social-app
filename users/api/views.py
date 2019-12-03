import logging

from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from users.decorators import func_log
from users.models import MyUser, UserProfile

from .permissions import IsOwnerOrReadOnly
from .serializers import RegistrationSerializer, UserProfileSerializer

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def registration_view(request):
    logger.debug(request)
    if request.method == 'POST':
        logger.debug(request.data)
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Success'
            data['email'] = user.email
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    RetrieveUpdateAPIView instead of RetrieveUpdateDestroyAPIView,
    because there is no need in deleting UserProfile object. 
    When we delete User object UserProfile gets destroyed on cascade.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # No allowing PUT method, because UserProfile should be only created when User is created.
    http_method_names = ('get', 'patch')

    def get_object(self, username):
        try:
            user = MyUser.objects.get(username=username)
            logger.debug(user)
            userprofile = UserProfile.objects.get(user=user)
            logger.debug(userprofile)
            return userprofile
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, username, format=None):
        userprofile = self.get_object(username)
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data)

    def patch(self, request, username, format=None):
        logger.debug(request.data)
        userprofile = self.get_object(username)
        self.check_object_permissions(self.request, userprofile)
        serializer = UserProfileSerializer(
            userprofile, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllUsersApiView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    permission_classes = (AllowAny, )


class UserProfilesView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    '''
    Mixins are containers of functionality, that you can include in class to provide some functionality in this view.
    We always include them at the beggining of our inheritance.
    '''

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)


class UserProfilesCreateView(
        mixins.ListModelMixin,
        generics.CreateAPIView):
    '''
     This is the same as UserProfileView, but we don't have to overider post()
    beacuse we are inheriting it.
    It does not handle GET method. But we can I it by ourselves.
    Like this:
    '''
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)


class UserProfilesPostListCreateView(generics.ListAPIView):
    ''' This one has the exact same functionallity like UserProfileView and UserProfileCreateView
    but we inherit from other generic so we have to write less code.
    '''
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class ApiUserProfileView(APIView):
    permission_classes = (IsAuthenticated, )

    @func_log
    def get(self, request, token, *args, **kwargs):
        print(token)
        print(request)
        print(request.data)

        qs = UserProfile.objects.all()
        serializer = UserProfileSerializer(qs, many=True)
        return Response(serializer.data)


class TestView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, username, format=None):
        logger.debug('with username')
        logger.debug(request.user)
        logger.debug(request.auth)
        logger.debug(request.data)
        logger.debug(username)
        logger.debug(dir(request))

        userprofile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(userprofile)

        response = serializer.data.copy()
        response['username'] = request.user.username
        response['email'] = request.user.email
        del response['user']
        return Response(response)
        # return Response(serializer.data)

    # def get(self, request, *args, **kwargs):
    #     logger.debug(request.user)
    #     logger.debug(request.auth)
    #     logger.debug(request.data)
    #     logger.debug(request.query_params)
    #     logger.debug(dir(request))

    #     userprofile = UserProfile.objects.get(user=request.user)
    #     serializer = UserProfileSerializer(userprofile)

    #     response = serializer.data.copy()
    #     response['username'] = request.user.username
    #     response['email'] = request.user.email
    #     del response['user']
    #     return Response(response)
        # return Response(serializer.data)

    @func_log
    def post(self, request, *args, **kwargs):
        logger.debug(request.data)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    # @func_log
    # def post(self, request, *args, **kwargs):
    #     logger.debug(request.data)
    #     serializer = RegistrationSerializer(data=request.data)
    #     data = {}
    #     if serializer.is_valid():
    #         user = serializer.save()
    #         data['response'] = 'Successfully registered a new user'
    #         data['emial'] = user.email
    #         data['username'] = user.username
    #     else:
    #         data = serializer.errors
    #     return Response(data)
        # serializer = RegistrationSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# # @permission_classes((IsAuthenticated,))
# def registration_view(request):
#     logger.debug(request)
#     if request.method == 'POST':
#         logger.debug(request.data)
#         serializer = RegistrationSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             user = serializer.save()
#             data['response'] = 'Successfully registered a new user'
#             data['emial'] = user.email
#             data['username'] = user.username
#             token = Token.objects.get(user=user).key
#             data['token'] = token
#         else:
#             data = serializer.errors
#         return Response(data)
