from addok import hooks

from .utils import (extend_results_removing_numbers,
                    extend_results_removing_one_whole_word,
                    extend_results_removing_succesive_trigrams, trigramize,
                    housenumber_field_key, match_housenumber)


@hooks.register
def addok_preconfigure(config):
    # We totally replace this logic.
    blacklist = ['addok.pairs', 'addok.fuzzy', 'addok.autocomplete']
    print('[addok-trigrams] Blocking plugins {}'.format(blacklist))
    for name in blacklist:
        config.pm.set_blocked(name)


@hooks.register(trylast=True)
def addok_configure(config):
    # Do not split housenumbers string in trigrams as document keys (i.e.
    # we want "19bis" once, and not "19b", "9bi", and so on).
    from addok.helpers import keys
    setattr(keys, 'housenumber_field_key', housenumber_field_key)
    target = 'addok.helpers.collectors.extend_results_reducing_tokens'
    if target in config.RESULTS_COLLECTORS:
        config.RESULTS_COLLECTORS.remove(target)
    config.RESULTS_COLLECTORS.append(extend_results_removing_numbers)
    config.RESULTS_COLLECTORS.append(extend_results_removing_one_whole_word)
    config.RESULTS_COLLECTORS.append(extend_results_removing_succesive_trigrams)
    config.PROCESSORS.append(trigramize)
    target = 'addok.helpers.results.match_housenumber'
    if target in config.SEARCH_RESULT_PROCESSORS:
        idx = config.SEARCH_RESULT_PROCESSORS.index(target)
        config.SEARCH_RESULT_PROCESSORS[idx] = match_housenumber
