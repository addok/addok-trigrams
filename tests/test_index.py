import json

from addok import ds
from addok.batch import process_documents
from addok.db import DB


def index_document(doc):
    process_documents(json.dumps(doc))


def deindex_document(_id):
    process_documents(json.dumps({'_id': _id, '_action': 'delete'}))


DOC = {
    'id': 'xxxx',
    '_id': 'xxxx',
    'type': 'street',
    'name': 'rue des Lilas',
    'city': 'Andrésy',
    'lat': '48.32545',
    'lon': '2.2565',
    'housenumbers': {
        '1': {
            'lat': '48.325451',
            'lon': '2.25651'
        }
    }
}


def test_index_document():
    index_document(DOC.copy())
    assert ds._DB.exists('d|xxxx')
    assert ds._DB.type('d|xxxx') == b'string'
    assert DB.exists('w|rue')
    assert b'd|xxxx' in DB.zrange('w|rue', 0, -1)
    assert DB.exists('w|des')
    assert DB.exists('w|lil')
    assert DB.exists('w|ila')
    assert DB.exists('w|las')
    assert DB.exists('w|and')
    assert DB.exists('w|ndr')
    assert DB.exists('w|dre')
    assert DB.exists('w|res')
    assert DB.exists('w|esy')
    assert DB.exists('g|u09dgm7')
    assert b'd|xxxx' in DB.smembers('g|u09dgm7')
    assert DB.exists('f|type|street')
    assert b'd|xxxx' in DB.smembers('f|type|street')
    assert DB.exists('f|type|housenumber')
    assert b'd|xxxx' in DB.smembers('f|type|housenumber')
    assert len(DB.keys()) == 13


def test_deindex_document_should_deindex():
    index_document(DOC.copy())
    deindex_document(DOC['id'])
    assert not ds._DB.exists('d|xxxx')
    assert not DB.exists('w|des')
    assert not DB.exists('w|lil')
    assert not DB.exists('w|ila')
    assert not DB.exists('w|las')
    assert not DB.exists('w|and')
    assert not DB.exists('w|ndr')
    assert not DB.exists('w|dre')
    assert not DB.exists('w|res')
    assert not DB.exists('w|esy')
    assert not DB.exists('g|u09dgm7')
    assert not DB.exists('f|type|street')
    assert not DB.exists('f|type|housenumber')
    assert len(DB.keys()) == 0


def test_deindex_document_should_not_affect_other_docs():
    DOC2 = {
        'id': 'xxxx2',
        '_id': 'xxxx2',
        'type': 'street',
        'name': 'rue des Lilas',
        'city': 'Paris',
        'lat': '49.32545',
        'lon': '4.2565',
        'housenumbers': {
            '1': {
                'lat': '48.325451',  # Same geohash as DOC.
                'lon': '2.25651'
            }
        }
    }
    index_document(DOC.copy())
    index_document(DOC2)
    deindex_document(DOC['id'])
    assert not ds._DB.exists('d|xxxx')
    assert DB.exists('w|rue')
    assert DB.exists('w|des')
    assert DB.exists('w|lil')
    assert b'd|xxxx' not in DB.zrange('w|rue', 0, -1)
    assert b'd|xxxx' not in DB.zrange('w|des', 0, -1)
    assert b'd|xxxx' not in DB.zrange('w|lil', 0, -1)
    assert b'd|xxxx' not in DB.zrange('w|un', 0, -1)
    assert DB.exists('g|u09dgm7')
    assert b'd|xxxx' not in DB.smembers('g|u09dgm7')
    assert b'd|xxxx2' in DB.zrange('w|rue', 0, -1)
    assert b'd|xxxx2' in DB.zrange('w|des', 0, -1)
    assert b'd|xxxx2' in DB.zrange('w|lil', 0, -1)
    assert b'd|xxxx2' in DB.smembers('g|u09dgm7')
    assert b'd|xxxx2' in DB.smembers('g|u0g08g7')
    assert DB.exists('f|type|street')
    assert b'd|xxxx2' in DB.smembers('f|type|street')
    assert DB.exists('f|type|housenumber')
    assert b'd|xxxx2' in DB.smembers('f|type|housenumber')
    assert len(DB.keys()) == 12


def test_index_housenumber_uses_housenumber_preprocessors():
    # By default it glues ordinal to number
    doc = {
        'id': 'xxxx',
        '_id': 'xxxx',
        'type': 'street',
        'name': 'rue des Lilas',
        'city': 'Paris',
        'lat': '49.32545',
        'lon': '4.2565',
        'housenumbers': {
            '1 bis': {
                'lat': '48.325451',
                'lon': '2.25651'
            }
        }
    }
    index_document(doc)
    saved = ds.get_document('d|xxxx')
    assert saved['housenumbers']['1bis'] == {
        'lat': '48.325451', 'lon': '2.25651', 'raw': '1 bis'}


# def test_allow_list_values():
#     doc = {
#         'id': 'xxxx',
#         'type': 'street',
#         'name': ['Vernou-la-Celle-sur-Seine', 'Vernou'],
#         'city': 'Paris',
#         'lat': '49.32545',
#         'lon': '4.2565'
#     }
#     index_document(doc)
#     assert DB.zscore('w|ver', 'd|xxxx') == 4
#     assert DB.zscore('w|sel', 'd|xxxx') == 4 / 5


def test_deindex_document_should_deindex_list_values():
    doc = {
        'id': 'xxxx',
        '_id': 'xxxx',
        'type': 'street',
        'name': ['Vernou-la-Celle-sur-Seine', 'Vernou'],
        'city': 'Paris',
        'lat': '49.32545',
        'lon': '4.2565'
    }
    index_document(doc)
    deindex_document(doc['id'])
    assert not ds._DB.exists('d|xxxx')
    assert not DB.exists('w|ver')
    assert not DB.exists('w|sel')
    assert len(DB.keys()) == 0


def test_doc_with_null_value_should_not_be_index_if_not_allowed(config):
    config.FIELDS = [
        {'key': 'name', 'null': False},
        {'key': 'city'},
    ]
    doc = {
        'id': 'xxxx',
        'lat': '49.32545',
        'lon': '4.2565',
        'name': '',
        'city': 'Cergy'
    }
    index_document(doc)
    assert not DB.exists('d|xxxx')


def test_null_value_should_not_be_index(config):
    doc = {
        'id': 'xxxx',
        'lat': '49.32545',
        'lon': '4.2565',
        'name': 'Port-Cergy',
        'city': ''
    }
    index_document(doc)
    assert 'city' not in DB.hgetall('d|xxxx')


def test_field_with_only_non_alphanumeric_chars_is_not_indexed():
    doc = {
        'id': 'xxxx',
        'lat': '49.32545',
        'lon': '4.2565',
        'name': 'Lilas',
        'city': '//'
    }
    index_document(doc)
    assert 'city' not in DB.hgetall('d|xxxx')
