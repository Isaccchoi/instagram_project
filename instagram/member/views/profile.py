from django.http import HttpResponse

from ..decorators import login_required

__all__ = (
    'profile',
)


@login_required
def profile(request):
    return HttpResponse(f'User profile page {request.user}')
