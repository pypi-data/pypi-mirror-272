import requests

class Word:
    def __init__(self, definition, permalink, thumbs_up, author, word, defid, current_vote, written_on, example, thumbs_down) -> None:
        self.word = word
        self.definition = definition
        self.example = example
        self.author = author
        self.permalink = permalink
        self.thumbs_up = thumbs_up
        self.thumbs_down = thumbs_down
        self.current_vote = current_vote
        self.written_on = written_on
        self.defid = defid
    def bracketless(self):
        edited_definition = self.definition
        edited_definition = edited_definition.replace('[', '')
        edited_definition = edited_definition.replace(']', '')
        self.definition = edited_definition
        return self

class SearchUD:
    def __init__(self, *word) -> None:
        if word == None:
            self.link = "https://api.urbandictionary.com/v0/random"
        else:
            self.link = f"https://api.urbandictionary.com/v0/define?term={word}"
        
    
    def start(self) -> list:
        self.data = requests.get(self.link).json()
        self.result = []        
        for i in self.data['list']:
            args = list(i.values())
            self.result.append(Word(*args))
        return self.result

if __name__ == '__main__':
    definitions = SearchUD('iswearitdoesntexiststhere').start()
    print(definitions)
