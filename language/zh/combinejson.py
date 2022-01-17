import json
import glob


def combine_jsons():
    """
    Combine all json files in current folder. Generate result.json.
    :return: True
    """
    d = {}
    l = []
    read_files = glob.glob("*.json")

    for file in read_files:
        f = open(file, 'rb')
        d = json.load(f)
        l += d['data']
    d['data'] = l
    result = json.dumps((d))

    outfile = open("result.json", 'w')
    outfile.write(result)
    outfile.close()
    return True

m = combine_jsons()
