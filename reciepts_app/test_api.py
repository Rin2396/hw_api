"""Tests for methods in the main app."""
import pytest
import requests

from stuff import TIMEOUT, URL

ID = 'id'
NAME = 'name'
DESCRIPTION = 'description'
PRODUCTS = 'products'

test_create = (
    (
        {
            NAME: 'Omelette',
            DESCRIPTION: 'Simple and tasty omelette',
            PRODUCTS: 'Eggs, Milk, Salt',
        },
        [
            {
                NAME: 'Omelette',
                DESCRIPTION: 'Simple and tasty omelette',
                PRODUCTS: 'Eggs, Milk, Salt',
            },
        ],
    ),
)

test_update_data = (
    (
        {
            NAME: 'Updated Omelette',
            DESCRIPTION: 'Even tastier omelette',
            PRODUCTS: 'Eggs, Milk, Salt, Pepper',
        },
        204,
    ),
)

test_delete = (204,)


@pytest.mark.parametrize('reciepts_for_create, expected', test_create)
def test_create_reciept(reciepts_for_create: dict, expected: tuple) -> None:
    """Test create and get methods.

    Args:
        reciepts_for_create (dict): create parameters
        expected (tuple): expected output
    """
    requests.post(
        f'{URL}/reciepts/create',
        json=reciepts_for_create,
        timeout=TIMEOUT,
    )

    response = requests.get(f'{URL}/reciepts', timeout=TIMEOUT)
    response = {key: value for key, value in response.json()[-1].items() if key != 'id'}
    expected = {key: value for key, value in expected[0].items() if key != 'id'}

    assert response == expected


@pytest.mark.parametrize('reciepts_for_update, expected', test_update_data)
def test_update_reciept(reciepts_for_update: dict, expected: int) -> None:
    """Test update method.

    Args:
        reciepts_for_update (dict): update parameters
        expected (int): expected response code
    """
    response = requests.get(f'{URL}/reciepts', timeout=TIMEOUT).json()
    response_id = response[-1][ID]

    response_code = requests.put(
        f'{URL}/reciepts/update',
        json={ID: response_id} | reciepts_for_update,
        timeout=TIMEOUT,
    ).status_code

    assert response_code == expected


@pytest.mark.parametrize('expected_code', test_delete)
def test_delete_reciept(expected_code: int) -> None:
    """Test delete method.

    Args:
        expected_code (int): expected response code
    """
    response = requests.get(f'{URL}/reciepts', timeout=TIMEOUT).json()
    response_id = response[-1]['id']

    response_code = requests.delete(
        f'{URL}/reciepts/delete',
        json={'id': response_id},
        timeout=TIMEOUT,
    ).status_code

    assert response_code == expected_code
