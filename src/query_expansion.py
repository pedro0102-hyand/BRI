import nltk
from nltk.corpus import wordnet

try:
    wordnet.synsets("test")
except LookupError:
    nltk.download("wordnet")
    nltk.download("omw-1.4")


def get_synonyms(word: str, max_synonyms: int = 2) -> list[str]:

    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            candidate = lemma.name().lower().replace("_", " ")
            if candidate != word and " " not in candidate:
                synonyms.add(candidate)
        if len(synonyms) >= max_synonyms:
            break
    return list(synonyms)[:max_synonyms]


def expand_tokens(tokens: list[str], max_synonyms: int = 2) -> list[str]:

    expanded = list(tokens)
    for token in tokens:
        expanded.extend(get_synonyms(token, max_synonyms=max_synonyms))
    return expanded


if __name__ == "__main__":
    
    sample_tokens = ["man", "discovered", "treasure"]
    print(f"Tokens originais: {sample_tokens}")

    for t in sample_tokens:
        print(f"  Sinônimos de '{t}': {get_synonyms(t)}")

    expanded = expand_tokens(sample_tokens)
    print(f"\nTokens expandidos: {expanded}")
    print(f"Total: {len(sample_tokens)} -> {len(expanded)}")