import requests


class EventPlaygroundService:
    limit = 5
    base_url = "http://localhost:8000/api/"

    def get_users(self, page=1):
        query_params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}users/", params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user(self, user_id: int) -> None:
        response = requests.get(f"{self.base_url}users/{user_id}/")
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id: int, user_data: dict) -> dict:
        response = requests.patch(f"{self.base_url}users/{user_id}/", json=user_data)
        response.raise_for_status()
        return response.json()

    def check_availability(self):
        response = requests.get(f"{self.base_url}ping/")
        response.raise_for_status()

    def get_tiers(self):
        response = requests.get(f"{self.base_url}users/get_tiers/")
        response.raise_for_status()
        return response.json()

    def update_password(self, user_id: int, user_data: dict) -> dict:
        response = requests.patch(f"{self.base_url}users/{user_id}/", json=user_data)
        response.raise_for_status()
        return response.json()

# # --------------------- EVENTS -------------------------------------------------------------------------------------

    def get_events(self, page=1):
        params = dict(limit=self.limit, offset=(page - 1) * self.limit)
        response = requests.get(f"{self.base_url}all_events/", params=params)
        response.raise_for_status()
        return response.json()

    def get_event(self, event_id: int) -> None:
        response = requests.get(f"{self.base_url}all_events/{event_id}/")
        response.raise_for_status()
        return response.json()

    def update_ticket_count(self, event_id: int, ticket_data: dict) -> dict:
        response = requests.patch(f"{self.base_url}all_events/{event_id}/", json=ticket_data)
        response.raise_for_status()
        return response.json()


event_service = EventPlaygroundService()
