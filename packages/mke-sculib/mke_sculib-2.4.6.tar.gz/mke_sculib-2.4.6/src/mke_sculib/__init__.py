__version__ = '2.4.6'

from mke_sculib.scu import scu as scu_api, plot_tt
from mke_sculib.sim import scu_sim
from mke_sculib.stellarium_api import stellarium_api as stellar_api
from mke_sculib.sim import plot_motion_pyplot as plot_motion


def load(antenna_id, post_put_delay=0.0, debug=False, url_qry = 'http://10.98.76.45:8990/antennas', **kwargs):
    if not "requests" in locals():
        import requests

    assert antenna_id, 'need to give an antenna id'

    if antenna_id == 'test_antenna':
        return scu_sim(antenna_id, debug=debug)
    else:
        ip = requests.get(f'{url_qry}/{antenna_id}').json()['address']
        return scu_api(ip, post_put_delay=post_put_delay, debug=debug)