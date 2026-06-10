from trekking_and_tour_management_system.users.models import User


class UserService:

    @staticmethod
    def create_user(
        *,
        email,
        password,
        name,
        role="customer",
    ):
        return User.objects.create_user(
            email=email,
            password=password,
            name=name,
            role=role,
        )

    @staticmethod
    def update_user(
        user,
        **data,
    ):
        for attr, value in data.items():
            setattr(user, attr, value)

        user.save()

        return user

    @staticmethod
    def get_user_by_email(
        email,
    ):
        return User.objects.filter(
            email=email
        ).first()