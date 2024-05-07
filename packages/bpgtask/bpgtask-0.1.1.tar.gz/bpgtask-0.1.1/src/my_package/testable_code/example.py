from typing import Protocol


class ApiClient(Protocol):
    def get_address(self, user_id: int) -> str: ...


class UserApi:
    def get_address(self, user_id: int) -> str:
        return "123 Main St"


def get_user_address(user_id: int, api_client: ApiClient = UserApi()) -> str:
    return api_client.get_address(user_id)
