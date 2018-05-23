#!/usr/bin/env python

from six.moves import configparser
import pandas


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    filename = config.get('data', 'scimagojr_file')
    print('[*] reading file: {}'.format(filename))

    data = pandas.read_excel(filename)
    print(data)


if __name__ == "__main__":
    main()
