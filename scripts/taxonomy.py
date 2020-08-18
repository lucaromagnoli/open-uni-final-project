import argparse
import json

import pandas as pd

parser = argparse.ArgumentParser(description='')
parser.add_argument('--file', dest='filename')
args = parser.parse_args()


def generate_taxonomy(filename):
    xls = pd.ExcelFile(filename)
    colors = pd.read_excel(xls, 'Colors', header=None)[0].to_list()
    materials = pd.read_excel(xls, 'Materials', header=None)[0].to_list()
    bags = {k: [i for i in v if pd.notnull(i)] for k, v in
            pd.read_excel(xls, 'Bags').to_dict('list').items()}
    wallets = {k: [i for i in v if pd.notnull(i)] for k, v in
               pd.read_excel(xls, 'Wallets').to_dict('list').items()}
    shoes = {k: [i for i in v if pd.notnull(i)] for k, v in
             pd.read_excel(xls, 'Shoes').to_dict('list').items()}
    hats = {k: [i for i in v if pd.notnull(i)] for k, v in
            pd.read_excel(xls, 'Hats').to_dict('list').items()}
    taxonomy = {
        'categories': ['Bags', 'Wallets', 'Shoes', 'Hats'],
        'colors': colors,
        'materials': materials,
        'bags': bags,
        'wallets': wallets,
        'shoes': shoes,
        'hats': hats,
    }
    with open('taxonomy.json', 'w') as f:
        json.dump(taxonomy, f, indent=4)


def main():
    generate_taxonomy(args.filename)


if __name__ == '__main__':
    main()
