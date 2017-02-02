# Addok-trigrams

Alternative indexation pattern for Addok, based on trigrams.


# Installation

    # No pypi release yet.
    pip install git+https://github.com/addok/addok-trigrams


# Configuration

In your local configuration file:

- remove `extend_results_reducing_tokens` from RESULTS_COLLECTORS:

        from addok.config.default import RESULTS_COLLECTORS
        RESULTS_COLLECTORS.remove('addok.helpers.collectors.extend_results_reducing_tokens')

- add new RESULTS_COLLECTORS:

        RESULTS_COLLECTORS += [
            'addok_trigrams.extend_results_removing_numbers',
            'addok_trigrams.extend_results_removing_one_whole_word',
            'addok_trigrams.extend_results_removing_successive_trigrams',
        ]

- add `trigramize` to PROCESSORS:

        PROCESSORS = [
            …,
            'addok_trigrams.trigramize',
        ]

- replace `addok.helpers.results.match_housenumber` from SEARCH_RESULT_PROCESSORS
  by the trigram dedicated one (usually at the first place of the list):

        SEARCH_RESULT_PROCESSORS = [
            'addok_trigrams.match_housenumber',
            …,
        ]

- remove `addok.pairs.pairs_indexer` and `addok.pairs.housenumbers_pairs_indexer`
  from `INDEXERS`:

        from addok.config.default import INDEXERS
        INDEXERS.remove('addok.pairs.pairs_indexer')
        INDEXERS.remove('addok.pairs.housenumbers_pairs_indexer')

- remove `addok.pairs.pairs_deindexer` and `addok.pairs.housenumbers_pairs_deindexer`
  from `DEINDEXERS`:

        from addok.config.default import DEINDEXERS
        DEINDEXERS.remove('addok.pairs.pairs_deindexer')
        DEINDEXERS.remove('addok.pairs.housenumbers_pairs_deindexer')
