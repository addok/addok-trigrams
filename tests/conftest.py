def pytest_configure():
    print('Configuring trigrams')
    from addok.config import config
    from addok import hooks
    import addok_trigrams
    hooks.register(addok_trigrams)
    config.RESULTS_COLLECTORS_PYPATHS.remove('addok.helpers.collectors.extend_results_reducing_tokens')  # noqa
    config.RESULTS_COLLECTORS_PYPATHS += [
        'addok_trigrams.extend_results_removing_numbers',
        'addok_trigrams.extend_results_removing_one_whole_word',
        'addok_trigrams.extend_results_removing_successive_trigrams',
    ]
    config.PROCESSORS_PYPATHS += ['addok_trigrams.trigramize']
    config.INDEXERS_PYPATHS.remove('addok.pairs.PairsIndexer')
    config.INDEXERS_PYPATHS.remove('addok.autocomplete.EdgeNgramIndexer')
