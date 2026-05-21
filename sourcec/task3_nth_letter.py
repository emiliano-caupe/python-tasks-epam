def nth_char(words: list) -> str:
    if not words:
        return ""
    return "".join(word[n] for n, word in enumerate(words))


if __name__ == "__main__":
    print(nth_char(["yoda", "best", "has"]))  # yes
    print(nth_char([]))                        # ""
    print(nth_char(["a", "bo", "cod"]))        # abd
