from addok.core import search


def test_should_match_name(street):
    assert not search('Conflans')
    street.update(name='Conflans')
    results = search('Conflans')
    assert results
    result = results[0]
    assert result.name == 'Conflans'
    assert result.id == street['id']


def test_should_match_name_case_insensitive(street):
    assert not search('conflans')
    street.update(name='Conflans')
    assert search('conflans')


def test_should_match_name_with_accent(street):
    assert not search('andrésy')
    street.update(name='Andrésy')
    assert search('andrésy')


def test_should_match_name_without_accent(street):
    assert not search('andresy')
    street.update(name='Andrésy')
    assert search('andresy')


def test_should_give_priority_to_best_match(street, city):
    street.update(name="rue d'Andrésy")
    city.update(name='Andrésy')
    results = search('andresy')
    assert results[0].id == city['id']


def test_should_give_priority_to_best_match2(street, factory):
    street.update(name="rue d'Andrésy", city="Conflans")
    factory(name="rue de Conflans", city="Andrésy")
    results = search("rue andresy")
    assert len(results) == 2
    assert results[0].id == street['id']


def test_should_give_priority_to_best_match3(street, factory):
    street.update(name="rue de Lille", city="Douai")
    other = factory(name="rue de Douai", city="Lille")
    results = search("rue de lille douai")
    assert len(results) == 2
    assert results[0].id == street['id']
    results = search("rue de douai lille")
    assert len(results) == 2
    assert results[0].id == other['id']


def test_should_be_fuzzy(city):
    city.update(name="Andrésy")
    assert search('antresy')
    assert search('antresu')


def test_fuzzy_should_work_with_inversion(city):
    city.update(name="Andrésy")
    assert search('andreys')


def test_fuzzy_should_match_with_removal(city):
    city.update(name="Andrésy")
    assert search('andressy')


def test_should_give_priority_to_housenumber_if_match(housenumber):
    housenumber.update(name='rue des Berges')
    results = search('rue des berges')
    assert not results[0].housenumber
    results = search('11 rue des berges')
    assert results[0].housenumber == '11'
    assert results[0].type == 'housenumber'


def test_should_not_return_housenumber_if_number_is_also_in_name(housenumber):
    housenumber.update(name='rue du 11 Novembre')
    results = search('rue du 11 novembre')
    assert not results[0].housenumber
    results = search('11 rue du 11 novembre')
    assert results[0].housenumber == '11'


def test_return_housenumber_if_number_included_in_bigger_one(factory):
    factory(name='rue 1814',
            housenumbers={'8': {'lat': '48.3254', 'lon': '2.256'}})
    results = search('rue 1814')
    assert not results[0].housenumber
    results = search('8 rue 1814')
    assert results[0].housenumber == '8'


def test_should_do_autocomplete(street):
    street.update(name='rue de Wambrechies', city="Bondues")
    assert search('avenue wambre', autocomplete=True)
    assert search('wambre avenue', autocomplete=True)


def test_synonyms_should_be_replaced(street, monkeypatch):
    monkeypatch.setattr('addok.helpers.text.SYNONYMS',
                        {'bd': 'boulevard'})
    street.update(name='boulevard des Fleurs')
    assert search('bd')


def test_should_return_results_if_only_common_terms(factory, monkeypatch):
    monkeypatch.setattr('addok.config.COMMON_THRESHOLD', 3)
    monkeypatch.setattr('addok.config.BUCKET_LIMIT', 3)
    street1 = factory(name="rue de la monnaie", city="Vitry")
    street2 = factory(name="rue de la monnaie", city="Paris")
    street3 = factory(name="rue de la monnaie", city="Condom")
    street4 = factory(name="La monnaye", city="Saint-Loup-Cammas")
    results = search('rue de la monnaie')
    ids = [r.id for r in results]
    assert street1['id'] in ids
    assert street2['id'] in ids
    assert street3['id'] in ids
    assert street4['id'] not in ids


def test_not_found_term_is_autocompleted(factory, monkeypatch):
    monkeypatch.setattr('addok.config.COMMON_THRESHOLD', 3)
    monkeypatch.setattr('addok.config.BUCKET_LIMIT', 3)
    factory(name="rue de la monnaie", city="Vitry")
    assert search('rue de la mon')


def test_autocomplete_should_give_priority_to_nearby(factory, monkeypatch):
    monkeypatch.setattr('addok.config.BUCKET_LIMIT', 3)
    monkeypatch.setattr('addok.core.Search.SMALL_BUCKET_LIMIT', 2)
    expected = factory(name='Le Bourg', lat=48.1, lon=2.2, importance=0.09)
    factory(name='Le Bourg', lat=-48.1, lon=-2.2, importance=0.1)
    factory(name='Le Bourg', lat=8.1, lon=42.2, importance=0.1)
    factory(name='Le Bourg', lat=10, lon=20, importance=0.1)
    results = search('bou', lat=48.1, lon=2.2, limit=3)
    assert len(results) == 3
    ids = [r.id for r in results]
    assert expected['id'] in ids
