# proto_sheet/health.py
from django.db import connection
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse


@extend_schema(
    tags=['Health'],
    summary='Health check',
    description=(
        'Verifies database and cache connectivity. '
        'Returns 200 if all services are healthy, 503 if any is degraded.'
    ),
    auth=[],
    responses={
        200: OpenApiResponse(description='All services healthy'),
        503: OpenApiResponse(description='One or more services degraded'),
    },
)
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    checks = {}

    # ---- Postgres ----
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = f'error: {e}'

    # ---- Redis ----
    try:
        cache.set('health_check_probe', 'ok', 10)
        value = cache.get('health_check_probe')
        checks['cache'] = 'ok' if value == 'ok' else 'error: value mismatch'
    except Exception as e:
        checks['cache'] = f'error: {e}'

    # ---- Status HTTP ----
    all_ok = all(v == 'ok' for v in checks.values())
    http_status = (
        status.HTTP_200_OK if all_ok
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return Response(
        {
            'status': 'ok' if all_ok else 'degraded',
            'checks': checks,
        },
        status=http_status,
    )
