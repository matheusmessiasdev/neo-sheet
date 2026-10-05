from django_ratelimit.exceptions import Ratelimited
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Extends the DRF's standard exception handler to convert the exception
    'Ratelimited' (que o DRF trataria como 403) in a 429 JSON
    standardized response.
    """
    if isinstance(exc, Ratelimited):
        return Response(
            {
                'detail': 'Too many requests. Please try again later.',
                'code': 'rate_limit_exceeded',
            },
            status=429,
        )

    # Fallback to DRF standard behavior
    return exception_handler(exc, context)
