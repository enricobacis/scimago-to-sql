#!/usr/bin/env python

import sqlite3
import pandas


def convert(scimagofile, dbfile):

    print('[*] reading file: {}'.format(scimagofile))
    venue = pandas.read_excel(scimagofile)

    print('[*] normalizing column names')
    venue.columns = venue.columns.str.replace('(^\W+|\W+$)', '')
    venue.columns = venue.columns.str.replace('\W+', '_')

    print('[*] normalizing ISSNs (one entry per ISSN)')
    issns = venue.Issn.str.replace('\s*ISSN\s*', '').str.split(
        '\s*,\s*', expand=True).stack()
    indices = issns.index.get_level_values(0)
    venue = venue.loc[indices].copy()
    venue["Issn"] = issns.values

    print('[*] creating Venue_Category data')
    venue_category = venue.Categories.str.split('\s*;\s*', expand=True).stack()
    venue_category.index = venue_category.index.droplevel(1)
    venue_category = pandas.DataFrame(venue_category)
    # https://regex101.com/r/rd280S/1
    venue_category = venue_category[0].str.extract(
        r'^(?P<Category>.*?)(?:(?:\s*\()(?P<Quartile>Q\d)(?:\)))?$')

    with sqlite3.connect(dbfile) as connection:
        print('[*] creating Venue table in: {}'.format(dbfile))
        venue.to_sql('Venue', connection, index=True, index_label='venue_id')

        print('[*] creating Venue_Category table in: {}'.format(dbfile))
        venue_category.to_sql('Venue_Category', connection,
                              index=True, index_label='venue_id')


if __name__ == "__main__":
    from six.moves.configparser import ConfigParser
    config = ConfigParser()
    config.read('config.ini')
    convert(scimagofile=config.get('data', 'scimagojr_file'),
            dbfile=config.get('data', 'dbfile'))
