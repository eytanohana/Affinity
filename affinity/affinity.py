from requests import Session
from requests.auth import HTTPBasicAuth

from affinity import models
from affinity import urls


class Affinity:
    def __init__(self, api_key):
        self.session = Session()
        self.session.auth = HTTPBasicAuth('', api_key)

    def get_lists(self) -> list[models.List]:
        response = self.session.get(urls.LISTS)
        if response.ok:
            return [models.List(**ls) for ls in response.json()]
        else:
            response.raise_for_status()

    def get_list_by_name(self, name: str) -> models.List | None:
        all_lists = self.get_lists()
        for ls in all_lists:
            if ls.name == name:
                return ls
        return None

    def get_list_by_id(self, list_id: int) -> models.ListId:
        response = self.session.get(urls.LIST_BY_ID.format(list_id=list_id))
        if response.ok:
            return models.ListId(**response.json())
        else:
            response.raise_for_status()

    def get_list_entries(self,
                         list_id: int,
                         page_size: int = None,
                         page_token: str = None) -> (list[models.ListEntry], str | None):
        query_params = {}
        if page_size:
            query_params |= {'page_size': page_size}
        if page_token:
            query_params |= {'page_token': page_token}
        response = self.session.get(urls.LIST_ENTRIES.format(list_id=list_id), params=query_params)
        if not response.ok:
            response.raise_for_status()

        list_entries = response.json()
        next_page_token = None
        if isinstance(list_entries, dict):
            next_page_token = list_entries.get('next_page_token')
            list_entries = list_entries.get('list_entries')
        return [models.ListEntry(**entry) for entry in list_entries], next_page_token

    def get_list_entry_by_id(self, list_id: int, list_entry_id: int):
        response = self.session.get(urls.LIST_ENTRY_BY_ID.format(list_id=list_id, list_entry_id=list_entry_id))
        if response.ok:
            return models.ListEntry(**response.json())
        else:
            response.raise_for_status()

    def get_fields(self, *,
                   list_id: int = None,
                   value_type: int = None,
                   entity_type: int = None,
                   with_modified_names: bool = False,
                   exclude_dropdown_options: bool = False) -> list[models.Field]:
        query_params = {}
        if list_id is not None:
            query_params |= {'list_id': list_id}
        if value_type is not None:
            query_params |= {'value_type': value_type}
        if entity_type is not None:
            query_params |= {'entity_type': entity_type}
        if with_modified_names:
            query_params |= {'with_modified_names': with_modified_names}
        if exclude_dropdown_options:
            query_params |= {'exclude_dropdown_options': exclude_dropdown_options}

        response = self.session.get(urls.FIELDS, params=query_params)
        if response.ok:
            return [models.Field(**field) for field in response.json()]
        else:
            response.raise_for_status()


