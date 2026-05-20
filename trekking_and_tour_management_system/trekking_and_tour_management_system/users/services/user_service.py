from trekking_and_tour_management_system.users.models import User


class UserService:

    @staticmethod
    def create_user(**data):

        return User.objects.create(**data)

    @staticmethod
    def update_user(user, **data):

        for attr, value in data.items():
            setattr(user, attr, value)

        user.save()

        return user