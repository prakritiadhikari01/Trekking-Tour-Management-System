from trekking_and_tour_management_system.guide_applications.models import GuideApplication
from trekking_and_tour_management_system.users.models import User


class GuideApplicationService:

    @staticmethod
    def create_application(user, validated_data):
        return GuideApplication.objects.create(
            user=user,
            **validated_data
        )

    @staticmethod
    def approve_application(application: GuideApplication):

        application.status = GuideApplication.STATUS_APPROVED
        application.save()

        user = application.user
        user.role = "guide"
        user.save()

        return application

    @staticmethod
    def reject_application(application: GuideApplication, note=None):

        application.status = GuideApplication.STATUS_REJECTED
        application.admin_note = note
        application.save()

        return application