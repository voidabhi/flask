from binascii import crc32
from app import models, db
from os import path
import inflect
import yaml
 
 
MAX_ID = 1073741823  # 2 ** 30 -1
inf = inflect.engine()
 
 
def import_fixtures(files):
    for f in files:
        table_name = path.splitext(path.basename(f))[0]
        model_name = ''.join([i.title() for i in inf.singular_noun(table_name).split('_')])
        rows = yaml.load(open(f))
 
        if hasattr(models, model_name):
            model_class = getattr(models, model_name)
            for row in rows:
                row = auto_ids(row)
                model_class().assign(**row).save()
        elif hasattr(models, table_name):
            table_clause = getattr(models, table_name)
            for row in rows:
                row = auto_ids(row)
                insert = table_clause.insert().values(**row)
                db.session.execute(insert)
 
 
def auto_ids(row):
    for attr in row:
        if attr == 'id' or attr.endswith('_id'):
            value = row[attr]
            if isinstance(value, int) or value.isdigit():
                continue
            else:
                row[attr] = crc32(value.encode('UTF-8')) % MAX_ID
    return row
