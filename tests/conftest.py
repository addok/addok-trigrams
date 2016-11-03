def pytest_configure():
    print('Configuring trigrams')
    from addok.config import config
    from addok import hooks
    import addok_trigrams
    hooks.register(addok_trigrams)
    config.RESULTS_COLLECTORS.remove('addok.helpers.collectors.extend_results_reducing_tokens')  # noqa
    config.RESULTS_COLLECTORS += [
        'addok_trigrams.extend_results_removing_numbers',
        'addok_trigrams.extend_results_removing_one_whole_word',
        'addok_trigrams.extend_results_removing_successive_trigrams',
    ]
    config.PROCESSORS += ['addok_trigrams.trigramize']
    config.SEARCH_RESULT_PROCESSORS.remove('addok.helpers.results.match_housenumber')  # noqa
    config.SEARCH_RESULT_PROCESSORS.insert(0, 'addok_trigrams.match_housenumber')  # noqa
