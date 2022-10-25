from dotenv import load_dotenv
from pathlib import Path
from affinity import Affinity

import os


def main():
    load_dotenv(Path(__file__).parent / '.env')
    affinity_key = os.environ.get('AFFINITY_KEY')
    af = Affinity(api_key=affinity_key)


if __name__ == '__main__':
    main()


