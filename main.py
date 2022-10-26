from dotenv import load_dotenv
from pathlib import Path
from affinity import Affinity

import os


def main():
    load_dotenv(Path(__file__).parent / '.env')
    affinity_key = os.environ.get('AFFINITY_KEY')
    af = Affinity(api_key=affinity_key)
    all_lists = af.get_lists()
    specific_list = af.get_list_by_name('Davids Affinity Integrations Testing')
    specific_list_by_id = af.get_list_by_id(specific_list.id)
    next_token = None
    specific_list_all_entries, next_token = af.get_list_entries(specific_list.id, page_size=1, page_token=next_token)
    all_entries = specific_list_all_entries
    while next_token is not None:
        specific_list_all_entries, next_token = af.get_list_entries(specific_list.id, page_size=1, page_token=next_token)
        all_entries.extend(specific_list_all_entries)
    list_entry = af.get_list_entry_by_id(specific_list.id, all_entries[-1].id)
    specific_list_fields = af.get_fields(list_id=specific_list.id)
    field_vals = af.get_field_values(organization_id=list_entry.entity_id)
    print()



if __name__ == '__main__':
    main()


