from rest_framework import serializers

from common import models


class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, style={"input_type": "password"})

    class Meta:
        model = models.UserProfile
        fields = ("id", "username", "email", "role", "is_superuser", "password")

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        # 用來設定預設的 is_active
        validated_data["is_active"] = True
        user = models.UserProfile.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RolePermission
        fields = ("id", "role", "menus", "actions")
