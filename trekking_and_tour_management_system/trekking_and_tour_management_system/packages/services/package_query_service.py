from trekking_and_tour_management_system.packages.selectors.package_selectors import (
    get_available_packages,
    get_all_packages,
    search_available_packages,
    search_all_packages,
)


class PackageQueryService:

    @staticmethod
    def get_packages(user, query=None):

        is_admin = (
            user.is_authenticated
            and user.role == "admin"
        )

        if is_admin:

            return (
                search_all_packages(query)
                if query
                else get_all_packages()
            )

        return (
            search_available_packages(query)
            if query
            else get_available_packages()
        )