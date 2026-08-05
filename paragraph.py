raw_paragraph = input("Enter a paragraph: ").split()


words = [word.strip(".,!?;:") for word in raw_paragraph]

print("Removed punctuation:", words)
print("Total words:", len(words))
print("Unique words:", len(set(words)))

longest_word = max(words, key=len)
shortest_word = min(words, key=len)
print("Longest word:", longest_word)
print("Shortest word:", shortest_word)

duplicates = [word for word in set(words) if words.count(word) > 1]
print("Words appearing more than once:", duplicates)

print("Alphabetical order:", sorted(words))

search_word = input("Enter a word to search: ")
if search_word in words:
    print(f"'{search_word}' found in the paragraph.")
else:
    print(f"'{search_word}' not found in the paragraph.")