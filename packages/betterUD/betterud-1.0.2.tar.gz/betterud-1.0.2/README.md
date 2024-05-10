
# betterUD

A better solution to parse definitions from Urban Dictionary for python


## Installation

Install betterUD with pip

```bash
  pip install betterud
```

Note: requests are required to run the library, so ensure you've installed it:

```bash
  pip install requests
```
## Usage
The library contains two main classes SearchUD and Word. SearchUD has only one function .start() and is used to search words' definitions through Urban Dictionary's API. Returns a list of Word's objects.

Word has arguments .definition, .permalink, .thumbs_up, .author, .word, .defid, .current_vote, .written_on, .example, .thumbs_down:

```python
from betterud import *

definitions = SearchUD('word').start()
print(definitions[0].definition)

Output:

A versatile [declaration], originating (more or less) in hip-hop culture.

"Word" has no single meaning, but is used to convey a casual sense of affirmation, [acknowledgement], agreement, or to indicate that something has impressed you favorably.

Its usage among young blacks has been parodied [ad nauseam] among clueless suburban whites.
```

Also, Word has a function .bracketless(). This function is used to remove brackets from object's definition and return object itself.

```python
from betterud import *

definitions = SearchUD('word').start()
print(definitions[0].bracketless().definition)

Output:

A versatile declaration, originating (more or less) in hip-hop culture.

"Word" has no single meaning, but is used to convey a casual sense of affirmation, acknowledgement, agreement, or to indicate that something has impressed you favorably.

Its usage among young blacks has been parodied ad nauseam among clueless suburban whites.
```
If SearchUD didn't get any arguments, it'd return definitions for random words from Urban Dictionary:

```python
from betterud import *

definitions = SearchUD().start()
print(definitions[0].word)

Output:

Came
```

If SearchUD didn't find a definition, it'd return an empty array:

```python
from betterud import *

definitions = SearchUD('iswearitdoesntexiststhere').start()
print(definitions)

Output:

[]
```


## Credits

Special thanks to atbuy, the creator of python_urbandict as I used his library to understand basics
