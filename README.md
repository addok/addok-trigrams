# Addok-trigrams

Alternative indexation pattern for Addok, based on trigrams.


# Installation

    # No pypi release yet.
    pip install git+https://github.com/addok/addok-trigrams


# Configuration

In your local configuration file:

- blacklist `pairs`, `fuzzy` and `autocomplete` internal plugins

        BLOCKED_PLUGINS = ['addok.pairs', 'addok.fuzzy', 'addok.autocomplete']

- remove `extend_results_reducing_tokens` from RESULTS_COLLECTORS

- add new RESULTS_COLLECTORS:

        RESULTS_COLLECTORS = [
            …,
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
