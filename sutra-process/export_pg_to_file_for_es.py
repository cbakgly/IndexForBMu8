import psycopg2
import settings
import argparse
import json

out_file = './es_data'


#读取参数
def read_args():
    parser = argparse.ArgumentParser(description="Search Elastic Engine")
    parser.add_argument("-o", dest="ofile", action="store", help="output file", default=out_file)
    return parser.parse_args()


def export(**kwargs):
    # clear all content

    with psycopg2.connect(database=settings.database, user=settings.user, password=settings.password, host=settings.host, port=settings.port) as conn:
        with conn.cursor() as cur:
            sql_temp = "select id,work_id,title,creator,creator_variant,vol_id,category,sutra_body from sutra order by id asc"
            cur.execute(sql_temp)
            # print(cur.query)

            result = cur.fetchall()

            if result is None:
                exit(1)

            size = 0;
            seq = 0;
            for row in result:
                print("eat row %s" % row[0])
                size += len(row[7]) if row[7] is not None else 0
                
                if size > 5 * 1024 * 1024:
                    seq += 1;
                    size = 0;

                with open(kwargs['ofile'] + str(seq), mode='a+', encoding='utf-8') as fp:
                    fp.writelines('{ "index":  { "_index": "%s", "_type": "%s", "_id": "%s" }}\n' % (settings.es_index, settings.es_type, row[0]))
                    fp.writelines('{ "work_id": "%s", "title": "%s", "creator": "%s", "creator_variant": "%s", "vol_id": "%s", "category": "%s", "sutra": %s}\n'
                                  % (row[1], row[2], row[3], row[4], row[5], row[6], json.dumps(row[7])))


if __name__ == '__main__':
    args = read_args()
    export(ofile = args.ofile)
    print('done')