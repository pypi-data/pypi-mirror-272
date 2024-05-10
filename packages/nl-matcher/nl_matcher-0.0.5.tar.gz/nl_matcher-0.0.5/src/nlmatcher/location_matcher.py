import spacy
from spacy.tokens import Span
from spacy.matcher import Matcher
from pathlib import Path
from .patterns import patterns
import re


class LocationMatcher():
    def __init__(self):
        # Exclude all but essencial pipelines to improve performance.
        exclude = [
            # 'ner',
            # 'morphologizer',
            # 'tok2vec',
            'tagger',
            'parser',
            'entity_linker',
            'entity_ruler',
            'textcat',
            'textcat_multilabel',
            'lemmatizer',
            'trainable_lemmatizer',
            'attribute_ruler',
            'senter',
            'sentencizer',
            'transformer',
        ]

        nlp = spacy.load('nl_core_news_lg', exclude=exclude)
        ruler = nlp.add_pipe('entity_ruler', before='ner')
        ruler.from_disk((Path(__file__).parent / "./rules").resolve())

        matcher = Matcher(nlp.vocab)

        for index, pattern in enumerate(patterns):
            matcher.add(f"pattern_{index}", [pattern], greedy="LONGEST")

        self.nlp = nlp
        self.matcher = matcher

    def __call__(self, text: str) -> list[Span]:
        """ Find locations in the text. """

        # Remove newlines and extra spaces.
        # This is done to improve the performance of the matcher by
        # elminiating the effect of newlines and extra spaces on the
        # text.
        text = text.strip()
        text = text.replace('\n', ' ')
        text = re.sub(r'\s+', ' ', text)

        doc = self.nlp(text)
        matches = self.matcher(doc, as_spans=True)
        matches = list(matches)

        return matches
