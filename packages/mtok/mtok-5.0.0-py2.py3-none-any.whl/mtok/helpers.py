import json
from os import environ
from pathlib import Path

import requests

class Const :
    # local GitHub token absolute filepath $HOME/.g.json, I assume it is in the home directory
    lg = Path(environ['HOME']) / '.g.json'
    # GitHub username
    gu = 'imahdimir'
    g = 'g'

c = Const()

def get_g() :
    with open(c.lg , 'r') as fi :
        gt = json.load(fi)[c.g]
    return gt

def get_all_tokens_fr_tokens_repo() -> dict :
    """ Gets all tokens from the private tokens repo """
    gt = get_g()

    trg_repo = 'tokens'
    br = 'main'
    fn = 'main.json'
    url = ret_github_url_for_private_access_to_file(gt , trg_repo , br , fn)

    r = requests.get(url)
    j = r.json()

    return j

def ret_github_url_for_private_access_to_file(gt , trg_repo , brnch , fn) :
    return f'https://{c.gu}:{gt}@raw.githubusercontent.com/{c.gu}/{trg_repo}/{brnch}/{fn}'
