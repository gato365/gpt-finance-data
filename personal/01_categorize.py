import spacy

def extract_purchase_descriptions(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    descriptions = []

    for token in doc:
        # Check if the token is a noun or a proper noun
        if token.pos_ in ["NOUN", "PROPN"]:
            # Look for adjectives or numbers before the noun
            desc = [token]
            for left_token in token.lefts:
                if left_token.dep_ in ["amod", "nummod"]:
                    desc.insert(0, left_token)
            descriptions.append(" ".join([t.text for t in desc]))

    return descriptions

if __name__ == "__main__":
    text = "I bought 3 red apples, a pair of shoes, and a blue bicycle."
    descriptions = extract_purchase_descriptions(text)
    print("Purchase descriptions:", descriptions)
