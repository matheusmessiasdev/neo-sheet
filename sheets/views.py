from .services.profile_template import PROFILE_BLANK_SCHEMA, PROFILE_TEMPLATE_SCHEMA, SCHEMAS_JSON_SCHEMA
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from django.http.request import HttpRequest
from .services.schema import base_schema
from .services.sheet_from_profile import configure_sheet_from_profile
from .models import ProfileModel
from .serializers import ProfileSerializer, ProfileListSerializer
from .permissions import IsUserOrReadOnly
from django.shortcuts import render
from django.db.models import Q
from django.http import Http404
# from jsonschema import validate
# from django.shortcuts import get_object_or_404
# Create your views here.


class ProfilesViewSet(viewsets.ModelViewSet):
    """
    List of system profiles avaliable.
    """
    http_method_names = ["get", "post", "patch", "delete"]
    # queryset = ProfileModel.objects.all().only("system_id", "display_name")

    lookup_field = "system_id"
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsUserOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        # Se o perfil não for oficial e o usuário não for o dono, levanta 404
        if not obj.is_official and obj.user != user:
            raise Http404("No Profile matches the given query.")
        return obj

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ProfileModel.objects.all().only("system_id", "display_name")

        return ProfileModel.objects.filter(Q(user_id=user.id) | Q(is_official=True)).only("system_id", "display_name")

    def perform_create(self, serializer: ProfileSerializer):
        user = self.request.user
        is_official = serializer.validated_data.get('is_official', False)
        if is_official and not user.is_staff:
            raise PermissionDenied("Only staff can create official profiles.")
        serializer.save(user=self.request.user,
                        is_official=is_official if user.is_staff else False)
        return super().perform_create(serializer)

    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PATCH" or \
                self.action == 'retrieve':
            return ProfileSerializer
        else:
            return ProfileListSerializer

    @action(detail=False)
    def blank_profile(self, request):
        """
        Base Profile used for creating a Profile.
        It is not a valid profile, as system_id and display_name must be filled.
        """
        return Response(PROFILE_BLANK_SCHEMA)
        ...

    @action(detail=False)
    def generic_sheet(self, request):
        """
        Schema that is returned from the base profiles created.
        """
        return Response(base_schema())

    @action(detail=False)
    def profile_template(self, request):
        """
        Profile template to auxiliate it's creation.
        """
        return Response(PROFILE_TEMPLATE_SCHEMA, status=status.HTTP_200_OK)

    @action(detail=True, url_path="sheet")
    def sheet_from_profile(self, request, **kwargs):
        system_id = kwargs.get("system_id") or self.kwargs.get("system_id")
        profile = self.get_object()
        return Response(configure_sheet_from_profile(profile))

    # def list(self, request):
    #     queryset = ProfileModel.objects.all().only("system_id", "display_name")
    #     serializer = ProfileListSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, system_id,  url_path="profile-detail"):
    #     profile = ProfileModel.objects.get(system_id=system_id)
    #     serializer = ProfileSerializer(profile)
    #     return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)

        return super().create(request, *args, **kwargs)


# TODO configurar o PATCH
# TODO configurar Soft Delete
