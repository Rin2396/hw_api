"""Extra functions for main app."""
import requests

from stuff import EXTRA_URL, OK, TIMEOUT

INGR_LENGTH = 13


def reciept_from_api(reciept_name):
    """Query reciept from api by name.

    Args:
        reciept_name: str - reciept's name

    Returns:
        dict: information about reciept
    """
    response = requests.get(f'{EXTRA_URL}{reciept_name}', timeout=TIMEOUT)
    if response.status_code == OK:
        return response.json()
    return None


def reciept_info(reciept_data, rec_name=None):
    """Get reciepts from database.

    Args:
        reciept_data: str - all reciepts
        rec_name: str - name of needed reciept. Defaults to None.

    Returns:
        dict: needed reciept or all reciepts
    """
    reciepts = []
    for reciept in reciept_data:
        rec = {}
        rec['id'] = reciept[0]
        rec['name'] = reciept[1]
        if rec_name is None or rec['name'] == rec_name:
            rec['description'] = reciept[2]
            rec['products'] = reciept[3]
            reciepts.append(rec)
    return reciepts


def reciept_info_from_api(reciept_data):
    """Get reciepts from api.

    Args:
        reciept_data: str - all reciepts

    Returns:
        dict: needed reciepts
    """
    reciepts = []
    for reciept in reciept_data['meals']:
        rec = {}
        rec['name'] = reciept['strMeal']
        rec['description'] = reciept['strInstructions']
        products = []
        for key, prod in reciept.items():
            if key[:INGR_LENGTH] == 'strIngredient' and prod:
                products.append(prod)
        rec['products'] = ', '.join(products)
        reciepts.append(rec)
    return reciepts
