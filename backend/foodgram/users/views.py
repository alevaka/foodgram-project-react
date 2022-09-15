from djoser.views import UserViewSet
from recipes.paginatons import CustomPagination
from rest_framework import generics, views
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Follow, User
from users.serializers import CustomUserSerializer, FollowUserSerializer


class CustomUserViewSet(UserViewSet):
    """Вьюсет для списка пользователей"""

    serializer_class = CustomUserSerializer
    queryset = User.objects.all()

    pagination_class = CustomPagination

    @action(detail=False, methods=['get'], name='subscriptions')
    def subscriptions(self, request):
        """Вывод списка подписок с рецептами"""

        user = request.user
        if user.is_authenticated:
            following_users = User.objects.filter(following__user=user)
            serializer = FollowUserSerializer(following_users,
                                              many=True,
                                              context={'request': request})
            return Response(serializer.data)
        return Response({'status': 'not authorized'})

    @action(detail=True, methods=['post', 'delete'], name='subscribe')
    def subscribe(self, request, username):
        """Добавление/удаление подписки на пользователей"""

        user = request.user
        user_id = (int(username) if (username.isdigit()) else 0)
        if not User.objects.filter(id=user_id).exists():
            return Response({'errors': 'Неверная ссылка!'},
                            status=views.status.HTTP_404_BAD_REQUEST)
        author = User.objects.get(id=user_id)

        if request.method == 'POST':
            if author != user:
                follow, status = Follow.objects.get_or_create(
                    user=user, author=author)
                if status:
                    serializer = CustomUserSerializer(author)
                    return Response(serializer.data,
                                    status=views.status.HTTP_201_CREATED)
                return Response({'errors': 'Вы уже подписаны!'},
                                status=views.status.HTTP_400_BAD_REQUEST)
            return Response({'errors': 'Нельзя подписаться на себя!'},
                            status=views.status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            if Follow.objects.filter(user=user, author=author).exists():
                Follow.objects.filter(user=user, author=author).delete()
                return Response({'status': 'Подписка отменена.'},
                                status=views.status.HTTP_204_NO_CONTENT)
            return Response({'errors': "Вы не подписаны!"},
                            status=views.status.HTTP_400_BAD_REQUEST)


class APIUserViewDetail(generics.RetrieveAPIView):
    """Вывод отдельного пользователя"""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
