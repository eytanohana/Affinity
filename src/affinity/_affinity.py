from requests import Session
from requests.auth import HTTPBasicAuth

from . import _models as models, _urls as urls


class Affinity:
    """
    The main object used to interact with the api.
    """
    def __init__(self, api_key):
        """
        :param api_key: The api key tied to your account.
        """
        self._session = Session()
        self._session.auth = HTTPBasicAuth('', api_key)

    def get_lists(self) -> list[models.List]:
        """
        Get a python list of all Affinity Lists.
        :return: A list of all Affinity Lists
        """
        response = self._session.get(urls.LISTS)
        if response.ok:
            return [models.List(**ls) for ls in response.json()]
        else:
            response.raise_for_status()

    def get_list_by_name(self, name: str) -> models.List | None:
        """
        Get a List by its name.
        :param name: The name of a specific List.
        :return: The specified List
        """
        all_lists = self.get_lists()
        for ls in all_lists:
            if ls.name == name:
                return ls
        return None

    def get_list_by_id(self, list_id: int) -> models.ListId:
        """
        Get a List by its ID
        :param list_id: The List ID
        :return: The List
        """
        response = self._session.get(urls.LIST_BY_ID.format(list_id=list_id))
        if response.ok:
            return models.ListId(**response.json())
        else:
            response.raise_for_status()

    def get_list_entries(self,
                         list_id: int,
                         *,
                         page_size: int = None,
                         page_token: str = None) -> (list[models.ListEntry], str | None):
        """
        Get all list entries for a specific List.
        :param list_id: The id of the list.
        :param page_size: The number of returned results
        :param page_token: A token to fetch the next pages results.
        :return: a list of Entries, next page token
        """
        query_params = {}
        if page_size:
            query_params |= {'page_size': page_size}
        if page_token:
            query_params |= {'page_token': page_token}
        response = self._session.get(urls.LIST_ENTRIES.format(list_id=list_id), params=query_params)
        if not response.ok:
            response.raise_for_status()

        list_entries = response.json()
        next_page_token = None
        if isinstance(list_entries, dict):
            next_page_token = list_entries.get('next_page_token')
            list_entries = list_entries.get('list_entries')
        return [models.ListEntry(**entry) for entry in list_entries], next_page_token

    def get_list_entry_by_id(self, list_id: int, list_entry_id: int) -> models.ListEntry:
        """
        Get a list entry by its id.
        :param list_id: The specific list id.
        :param list_entry_id: The list entry id.
        :return: The list entry.
        """
        response = self._session.get(urls.LIST_ENTRY_BY_ID.format(list_id=list_id, list_entry_id=list_entry_id))
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
        """
        Get a list of fields fitting the parameters filled in.
        :param list_id: the list id.
        :param value_type: the value type.
        :param entity_type: the entity type.
        :param with_modified_names: return the fields as List[Field Name].
        :param exclude_dropdown_options: exclude drop down options.
        :return: A list of fields.
        """
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

        response = self._session.get(urls.FIELDS, params=query_params)
        if response.ok:
            return [models.Field(**field) for field in response.json()]
        else:
            response.raise_for_status()

    def get_field_values(self, *,
                         person_id: int = None,
                         organization_id: int = None,
                         opportunity_id: int = None,
                         list_entry_id: int = None
                         ) -> list[models.FieldValue]:
        """
        Get a list of field values fitting the parameters given.
        :param person_id:  the person id.
        :param organization_id: the organization id.
        :param opportunity_id: the opportunity id.
        :param list_entry_id: the list entry id.
        :return: The list of field values.
        """
        if sum(bool(arg) for arg in (person_id, organization_id, opportunity_id, list_entry_id)) != 1:
            raise ValueError('Exactly one argument must be specified')
        if person_id is not None:
            query_params = {'person_id': person_id}
        elif organization_id is not None:
            query_params = {'organization_id': organization_id}
        elif opportunity_id is not None:
            query_params = {'opportunity_id': opportunity_id}
        else:
            query_params = {'list_entry_id': list_entry_id}

        response = self._session.get(urls.FIELD_VALUES, params=query_params)
        if response.ok:
            return [models.FieldValue(**field_val) for field_val in response.json()]
        else:
            response.raise_for_status()

    def get_persons(self, *,
                    term: str = None,
                    with_interaction_dates: bool = False,
                    with_interation_persons: bool = False,
                    with_opportunities: bool = False,
                    page_size: int = None,
                    page_token: str = None,
                    **kwargs) -> (list[models.Person], str | None):
        query_params = {k: v for k, v in locals().items()
                        if k not in {'self', 'query_params', 'kwargs'} and v is not None}
        query_params.update(kwargs)
        response = self._session.get(urls.PERSONS, params=query_params)
        if response.ok:
            res = response.json()
            people, next_page_token = res['persons'], res['next_page_token']
            return [models.Person(**pers) for pers in people], next_page_token
        else:
            response.raise_for_status()

    def get_person_by_id(self, person_id, *,
                         with_interaction_dates: bool = False,
                         with_interaction_persons: bool = False,
                         with_opportunities: bool = False) -> models.Person:
        query_params = {k: v for k, v in locals().items() if k not in {'self', 'query_params', 'person_id'}}
        response = self._session.get(urls.PERSON_BY_ID.format(person_id=person_id), params=query_params)
        if response.ok:
            return models.Person(**response.json())
        else:
            response.raise_for_status()

    def get_organizations(self, *,
                          term: str = None,
                          with_interaction_dates: bool = False,
                          with_interation_persons: bool = False,
                          with_opportunities: bool = False,
                          page_size: int = None,
                          page_token: str = None,
                          **kwargs):
        response = self._session.get(urls.ORGANIZATIONS)
        return response.json()
