# Addok-trigrams

Alternative indexation pattern for Addok, based on trigrams.


## Installation

    pip install addok-trigrams


## Configuration

In your local configuration file:

- remove `extend_results_reducing_tokens` from RESULTS_COLLECTORS_PYPATHS:

        from addok.config.default import RESULTS_COLLECTORS_PYPATHS
        RESULTS_COLLECTORS_PYPATHS.remove('addok.helpers.collectors.extend_results_reducing_tokens')

- add new RESULTS_COLLECTORS_PYPATHS:

        RESULTS_COLLECTORS_PYPATHS += [
            'addok_trigrams.extend_results_removing_numbers',
            'addok_trigrams.extend_results_removing_one_whole_word',
            'addok_trigrams.extend_results_removing_successive_trigrams',
        ]

- add `trigramize` to PROCESSORS_PYPATHS:

        PROCESSORS_PYPATHS += [
            'addok_trigrams.trigramize',
        ]

- remove pairs and autocomplete indexers from `INDEXERS_PYPATHS`:

        from addok.config.default import INDEXERS_PYPATHS
        INDEXERS_PYPATHS.remove('addok.pairs.PairsIndexer')
        INDEXERS_PYPATHS.remove('addok.autocomplete.EdgeNgramIndexer')


## Usage

Use `addok batch` just like with genuine addok for importing documents, but no
need for running `addok ngrams`, given they are already part of the index
strategy.
