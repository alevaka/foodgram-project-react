from djoser.serializers import UserSerializer
from rest_framework import serializers
from users.models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class FollowUserSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        return obj.following.filter(
            user=self.context.get('request').user).exists()

    def get_recipes(self, obj):
        from recipes.serializers import RecipeSerializer
        request = self.context.get('request')
        serializer_list = RecipeSerializer(
            obj.recipes.all(), many=True, read_only=True,
            context={'request': request})
        keys = ['id', 'name', 'image', 'cooking_time']
        return ([{key: serializer[key] for key in keys}
                for serializer in serializer_list.data])
