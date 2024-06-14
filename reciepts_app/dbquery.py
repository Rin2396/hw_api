"""Database queries."""
QUERY_GET_RECIEPTS = """
select
  rec.id,
  rec.name,
  rec.description,
  rec.products
from reciept_site.reciepts rec;
"""

QUERY_REC_CREATE = """
insert into reciept_site.reciepts(name, description, products)
values ({name}, {description}, {products})
returning id
"""

QUERY_UPDATE_RECIEPTS = """
update reciept_site.reciepts
set
  name = {name},
  description = {description},
  products = {products}
where id = {id}
returning id
"""

QUERY_DELETE_RECIEPT = 'delete from reciept_site.reciepts where id = {id} returning id'
