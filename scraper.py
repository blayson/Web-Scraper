import logging
import requests
import os
import urllib.request
import configparser


logging.basicConfig(level=logging.DEBUG)


def dir_management(new_dir, old_dir):
    os.chdir(old_dir)
    try:
        os.mkdir(new_dir)
        os.chdir(new_dir)
    except FileExistsError:
        os.chdir(new_dir)


def parse_species():
    owd = os.getcwd()
    config = configparser.ConfigParser()
    config.read('config.ini')
    site = config['DEFAULT']['url']
    for region in 'weurope', 'canada', 'namerica', 'antilles', 'guyane', \
                  'lapaz', 'afn', 'reunion', 'maurice', 'medor', 'hawai', 'salad':
        url = '{0}/api/project/{1}/getSpecies/ru'.format(site, region)
        species_resp = requests.get(url).json()
        for species in species_resp['species']:
            name = species['name']
            url_spec_details = "{0}/" \
                               "api/project/{1}/get_species_details/{2}/ru" \
                               "".format(site, region, requests.utils.quote(name))
            details_resp = requests.get(url_spec_details).json()

            dir_management(name, owd)
            odir = os.getcwd()

            for key, value in details_resp['imgs'].items():
                dir_management(key, odir)

                for item in value:
                    fname = item['id']
                    link = item['full_img']
                    urllib.request.urlretrieve(
                        link, '{}.jpg'.format(fname))

parse_species()
