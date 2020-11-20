from typing import List


def prefix_match(prompt: str, arr: List[str], key: str = None) -> str:
    if len(arr) == 0:
        print('No elements in search array.')
        return ""
    while True:
        if key is None:
            key = input(prompt)
        if key == "":
            return ""
        matches = [x for x in arr if key == x[:len(key)]]
        if len(matches) != 1:
            print(f'Matches: {"None" if len(matches) == 0 else matches}')
            if key is not None:
                return ""
            continue
        return matches[0]
