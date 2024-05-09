# NL Matcher

A simple library to match locations in text using SpaCy

## Installation

```bash
pip install nlmatcher
```

## Usage

```python
import nlmatcher

matcher = nlmatcher.LocationMatcher()

text = "I live in Amsterdam and work in Utrecht"
matches = matcher.match(text)

for match in matches:
    print(match.text)
```

## Output

```
Amsterdam
Utrecht
```
