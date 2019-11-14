import logging

from rest_framework import generics, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.decorators import func_log
from users.models import Profile

from .serializers import ProfileSerializer, RegistrationSerializer

# from .models import


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


class ProfileView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    '''
    Mixins are containers of functionality, that you can include in class to provide some functionality in this view.
    We always include them at the beggining of our inheritance.
    '''

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(self, request, *args, **kwargs)


class ProfileCreateView(
        mixins.ListModelMixin,
        generics.CreateAPIView):
    '''
     This is the same as ProfileView, but we don't have to overider post()
    beacuse we are inheriting it.
    It does not handle GET method. But we can I it by ourselves.
    Like this:
    '''
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(self, request, *args, **kwargs)


class ProfilePostListCreateView(generics.ListAPIView):
    ''' This one has the exact same functionallity like ProfileView and ProfileCreateView
    but we inherit from other generic so we have to write less code.
    '''
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class TestView(APIView):

    permission_classes = (IsAuthenticated, )

    @func_log
    def get(self, request, *args, **kwargs):
        qs = Profile.objects.all()
        serializer = ProfileSerializer(qs, many=True)
        return Response(serializer.data)

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
