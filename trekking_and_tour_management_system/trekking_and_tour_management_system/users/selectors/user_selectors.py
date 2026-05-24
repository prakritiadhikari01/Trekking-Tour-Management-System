from trekking_and_tour_management_system.users.models import User


def get_user_by_id(user_id):

    return User.objects.filter(id=user_id).first()


def get_all_users():

    return User.objects.all()
