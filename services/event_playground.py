import requests
#
#
# class UserPlaygroundService:
#     limit = 10
#     base_url_users = "http://127.0.0.1:8000/"
#
#     def get_users(self, page=1):
#         query_params = dict(limit=self.limit, offset=(int(page) - 1) * self.limit)
#         response = requests.get(f"{self.base_url_users}all_users", params=query_params)
#         response.raise_for_status()
#         return response.json()
#
#     def get_user(self, user_id):
#         response = requests.get(f"{self.base_url_users}all_users/{user_id}")
#         response.raise_for_status()
#         return response.json()
#
#
# user_service = UserPlaygroundService()
#
#
# class EventPlaygroundService:
#     limit = 10
#     base_url_events = 'http://127.0.0.1:8000/'
#
#     def get_events(self, page=1):
#         params = dict(limit=self.limit, offset=(int(page) - 1) * self.limit)
#         response = requests.get(f"{self.base_url_events}all_events", params=params)
#         response.raise_for_status()
#         return response.json()
#
#
# event_service = EventPlaygroundService()

# # -------------------------------------


class UserPlaygroundService:
    limit = 5
    base_url = "http://127.0.0.1:8000/"

    def get_users(self, page=1):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}all_users/", params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user(self, user_id: int) -> None:
        response = requests.get(f"{self.base_url}all_users/{user_id}/")
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id: int, user_data: dict) -> dict:
        response = requests.patch(f"{self.base_url}all_users/{user_id}/", json=user_data)
        response.raise_for_status()
        return response.json()


user_service = UserPlaygroundService()

# # ---------------------------- EVENTS -------------------------------------------------------------------------------


class EventPlaygroundService:
    limit = 5
    base_url_events = 'http://127.0.0.1:8000/'

    def get_events(self, page=1):
        params = dict(limit=self.limit, offset=(int(page) - 1) * self.limit)
        response = requests.get(f"{self.base_url_events}all_events", params=params)
        response.raise_for_status()
        return response.json()

    def get_event(self, event_id: int) -> None:
        response = requests.get(f"{self.base_url_events}all_events/{event_id}/")
        response.raise_for_status()
        return response.json()


event_service = EventPlaygroundService()
