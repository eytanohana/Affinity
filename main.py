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
    print()



if __name__ == '__main__':
    main()


