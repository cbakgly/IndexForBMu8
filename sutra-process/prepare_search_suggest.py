import settings
import argparse
import json

out_file = './es_suggest'


#读取参数
def read_args():
    parser = argparse.ArgumentParser(description="Search Elastic Engine")
    parser.add_argument("-o", dest="ofile", action="store", help="output file", default=out_file)
    parser.add_argument("-i", dest="ifile", action="store", help="input file", required=True)
    return parser.parse_args()


def export(**kwargs):
    # clear all content

    with open(kwargs['ifile'], mode='r', encoding='utf-8') as ifp:
        size = 0
        seq = 0
        id = 0
        for line in ifp:
            print("eat row %s" % line)
            id += 1
            size += len(line)
            
            if size > 5 * 1024 * 1024:
                seq += 1
                size = 0

            with open(kwargs['ofile'] + str(seq), mode='a+', encoding='utf-8') as fp:
                fp.writelines('{ "index":  { "_index": "%s", "_type": "%s", "_id": "%s" }}\n' % (settings.es_index, settings.es_type_suggest, id))
                fp.writelines('{ "candidate": "%s", "search_count": 0}\n' % (line.strip()))


if __name__ == '__main__':
    args = read_args()
    export(ofile = args.ofile, ifile = args.ifile)
    print('done')