"""
View Set
"""

from rest_framework import exceptions, viewsets

import bases.permissions
from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    User View Set: crate, update, get and list
    """
    permission_classes = [bases.permissions.IsPostOrIsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        """
        Get only to own user.
        - Only the owner and staff can get a user
        """
        pk = self.kwargs['pk']
        if pk == 'me' or pk == str(self.request.user.id):
            return self.request.user
        else:
            if self.request.user.is_staff:
                try:
                    return User.objects.get(id=pk)
                except User.DoesNotExist:
                    raise exceptions.NotFound()

        raise exceptions.PermissionDenied()

    def list(self, request, *args, **kwargs):
        """
        Only Staff can get a list in the user endpoint
        """
        if not request.user.is_staff:
            raise exceptions.PermissionDenied()

        return super(UserViewSet, self).list(request, *args, **kwargs)
