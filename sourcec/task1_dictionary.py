class Dictionary:
    def __init__(self):
        self.entries = {}

    def newentry(self, word: str, definition: str):
        self.entries[word] = definition

    def look(self, word: str) -> str:
        if word in self.entries:
            return self.entries[word]
        return f"Can't find entry for {word}"


if __name__ == "__main__":
    d = Dictionary()
    d.newentry('Apple', 'A fruit that grows on trees')
    print(d.look('Apple'))
    print(d.look('Banana'))
