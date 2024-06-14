"""My app for reciepts."""
from flask import render_template, request
from psycopg2 import OperationalError
from psycopg2.sql import SQL, Literal

import dbquery
from creds import FLASK_PORT, app, connection
from functions import reciept_from_api, reciept_info, reciept_info_from_api
from stuff import NO_CONTENT, NOT_FOUND, OK, SERVER_ERROR

connection.autocommit = True


@app.route('/')
def welcomepage():
    """Show welcome page.

    Returns:
        str: render a template by name
    """
    get_reciepts()
    try:
        data = get_reciepts()
    except Exception:
        return '<h1>Something wrong</h1>', SERVER_ERROR

    return render_template(
        'index.html',
        title='home',
        reciepts=data,
    )


@app.get('/reciepts')
def get_reciepts():
    """Query get method.

    Returns:
        dict: reciepts information
    """
    reciept_name = request.args.get('name')
    try:
        with connection.cursor() as cursor:
            cursor.execute(dbquery.QUERY_GET_RECIEPTS)
            result = cursor.fetchall()
        if result:
            recs = reciept_info(result, reciept_name)
            if recs:
                return recs
        if reciept_name:
            external_reciept = reciept_from_api(reciept_name)
            if external_reciept:
                return reciept_info_from_api(external_reciept)
    except OperationalError:
        return SERVER_ERROR


@app.post('/reciepts/create')
def create_reciept():
    """Query post method.

    Returns:
        tuple: result and status code
    """
    body = request.json

    name = body['name']
    description = body['description']
    products = body['products']

    query = SQL(dbquery.QUERY_REC_CREATE).format(
        name=Literal(name),
        description=Literal(description),
        products=Literal(products),
        )

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    return result, OK


@app.put('/reciepts/update')
def update_reciepts():
    """Query put method.

    Returns:
        tuple: blank and status code
    """
    body = request.json

    id_ = body['id']
    name = body['name']
    description = body['description']
    products = body['products']

    query = SQL(dbquery.QUERY_UPDATE_RECIEPTS).format(
        id=Literal(id_),
        name=Literal(name),
        description=Literal(description),
        products=Literal(products),
        )

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()

    if not result:
        return '', NOT_FOUND

    return '', NO_CONTENT


@app.delete('/reciepts/delete')
def delete_reciept():
    """Query delete methid.

    Returns:
        tuple: blank and status code
    """
    body = request.json

    id_ = body['id']

    delete_reciept = SQL(dbquery.QUERY_DELETE_RECIEPT).format(id=Literal(id_))

    with connection.cursor() as cursor:
        cursor.execute(delete_reciept)
        result = cursor.fetchall()

    if not result:
        return '', NOT_FOUND

    return '', NO_CONTENT


if __name__ == '__main__':
    app.run(port=FLASK_PORT)
