import os.path
import re
import psycopg2

import settings
basedir = '/Users/me866/Repo/dzj/BM_u8_out'


with psycopg2.connect(database=settings.database, user=settings.user, password=settings.password, host=settings.host, port=settings.port) as conn:
    with conn.cursor() as cur:
        for parent, dirnames, filenames in os.walk(basedir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
            for filename in filenames:
                parent_dir = parent
                filename = filename
                filepath = os.path.join(parent, filename)

                if filename[0] == '.':
                    continue

                loc = re.findall('([a-zA-Z]{1,2})([0-9]*)n([0-9a-zA-Z]{1,4})', filename)
                work_id = loc[0][0] + loc[0][2]

                sql_temp = "update sutra set sutra_body = concat(sutra_body, %s) where work_id = %s "

                with open(filepath) as f:
                    print(filepath)
                    content = f.read()
                cur.execute(sql_temp, [content, work_id])

