"""Launch web functionnal test of monstericon application

Usage:
  functionnal_tests.py <base_url>
"""

from docopt import docopt
import requests

if __name__ == '__main__':
    arguments = docopt(__doc__)

    response = requests.get(arguments['<base_url>'])

    assert response.status_code == 200
    assert 'Monster Icon' in response.text

    response2 = requests.get(arguments['<base_url>']+'/monster/test')

    assert response2.status_code == 200

    print("Application seems Ok :)")
