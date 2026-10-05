from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from .services.profile_template import PROFILE_BLANK_SCHEMA, PROFILE_TEMPLATE_SCHEMA
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
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
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.core.cache import cache
# Create your views here.


@extend_schema_view(
    list=extend_schema(
        tags=['Profiles'],
        # ← opcional (leitura pública/autenticada)
        auth=[{"BearerAuth": []}, {}],
        summary='List profiles',
        description='Returns a list of available profiles. Authenticated users see official profiles + their own. Anonymous users see only official profiles.',
        responses={200: ProfileListSerializer(many=True)},
    ),
    create=extend_schema(
        tags=['Profiles'],
        auth=[{"BearerAuth": []}],  # ← OBRIGATÓRIO (não opcional!)
        summary='Create Profile',
        description='Creates a new system profile. Only authenticated users can create profiles. Only staff can create official profiles.',
        request=ProfileSerializer,
        responses={201: ProfileSerializer},
    ),
    retrieve=extend_schema(
        tags=['Profiles'],
        auth=[{"BearerAuth": []}, {}],  # ← opcional
        summary='Detail profile',
        description='Returns the details of a specific profile. Private profiles are only visible to the owner.',
        responses={200: ProfileSerializer},
    ),
    update=extend_schema(
        tags=['Profiles'],
        auth=[{"BearerAuth": []}],  # ← OBRIGATÓRIO
        summary='Update profile (complete)',
        description='Updates all fields in a profile. Only the owner can update private profiles.',
        request=ProfileSerializer,
        responses={200: ProfileSerializer},
    ),
    partial_update=extend_schema(
        tags=['Profiles'],
        auth=[{"BearerAuth": []}],  # ← OBRIGATÓRIO
        summary='Update profile (partial)',
        description='Updates partially a profile. Only the owner can update private profiles.',
        request=ProfileSerializer,
        responses={200: ProfileSerializer},
    ),
    destroy=extend_schema(
        tags=['Profiles'],
        auth=[{"BearerAuth": []}],  # ← OBRIGATÓRIO
        summary='Deletes profile',
        description='Deletes a profile. Only the owner can delete a private profile.',
        responses={204: OpenApiResponse(
            description='Profile deleted successfully')},
    ),
)
@method_decorator(vary_on_headers('Authorization'), name='list')
@method_decorator(cache_page(60 * 5), name='list')
class ProfilesViewSet(viewsets.ModelViewSet):
    """
    List of system profiles avaliable.
    """
    http_method_names = ["get", "post", "patch", "delete"]

    lookup_field = "system_id"
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsUserOrReadOnly]

    def get_object(self):
        profile_obj = super().get_object()
        user = self.request.user
        if not profile_obj.is_official and profile_obj.user != user:
            raise Http404("No Profile matches the given query.")
        return profile_obj

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
        cache.clear()
        return super().perform_create(serializer)

    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PATCH" or \
                self.action == 'retrieve':
            return ProfileSerializer
        else:
            return ProfileListSerializer

    @extend_schema(
        tags=['Profiles'],
        summary='Empty template for creation',
        auth=[],
        description='Returns an empty template for creating a new profile. Serves as a starting point to understend the expected structure.',
        responses={200: OpenApiResponse(
            description='Empty Template', response=dict)},
    )
    @action(detail=False)
    def blank_profile(self, request):
        """
        Base Profile used for creating a Profile.
        It is not a valid profile, as system_id and display_name must be filled.
        """
        return Response(PROFILE_BLANK_SCHEMA)
        ...

    @extend_schema(
        tags=['Profiles'],
        summary='Global base schema',
        auth=[],
        description='Returns the base schema that servers for all profiles.',
        responses={200: OpenApiResponse(
            description='Base Schema', response=dict)},
    )
    @method_decorator(cache_page(60 * 15))
    @action(detail=False)
    def generic_sheet(self, request):
        """
        Schema that is returned from the base profiles created.
        """
        return Response(base_schema())

    @extend_schema(
        tags=['Profiles'],
        summary='Template with docs',
        auth=[],
        description='Returns the profile template with descriptions and examples, assisting creation.',
        responses={200: OpenApiResponse(
            description='Documentated template', response=dict)},
    )
    @action(detail=False)
    def profile_template(self, request):
        """
        Profile template to auxiliate it's creation.
        """
        return Response(PROFILE_TEMPLATE_SCHEMA, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Profiles'],
        summary='Creates sheet from profile',
        description='Creates a character sheet from a specific profile, with metadata removed.',
        responses={200: OpenApiResponse(
            description='Sheet created', response=dict)},
    )
    @action(detail=True, url_path="sheet")
    def sheet_from_profile(self, request, **kwargs):
        """
        Creates the sheet from the profile.
        """
        system_id = kwargs.get("system_id") or self.kwargs.get("system_id")
        profile = self.get_object()
        return Response(configure_sheet_from_profile(profile))

    def destroy(self, request, *args, **kwargs):

        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)

        return super().create(request, *args, **kwargs)
