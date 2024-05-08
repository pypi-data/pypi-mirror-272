

def count_enclosed_strings(s):
    open_index = -1  # To track the index of the last opened '<'
    in_tag = False  # Flag to check if we are currently within a tag
    total_count = 0  # Accumulate counts of all valid enclosed strings

    for i, char in enumerate(s):
        if char == '<':
            if in_tag:  # If already in a tag and see another '<', it's invalid
                raise ValueError("Invalid string: nested '<' found.")
            in_tag = True
            open_index = i
        elif char == '>':
            if not in_tag:  # If '>' appears without a preceding '<', it's invalid
                raise ValueError("Invalid string: unmatched '>'.")
            # Valid tag closed, count characters inside
            count = i - open_index - 1
            total_count += 1
            in_tag = False

    if in_tag:  # If we finished iterating and are still 'inside' a tag
        raise ValueError("Invalid string: unmatched '<'.")

    return total_count

if __name__ == '__main__':
    pass

