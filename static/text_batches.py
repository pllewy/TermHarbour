class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def size(self):
        return len(self.items)

    def __repr__(self):
        return f"Stack({self.items})"


def write_batches_to_file_as_list(batches, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("[\n")
        for batch in batches:
            file.write(f"    {repr(batch)},\n")
        file.write("]\n")


def create_text_batches(source_text, target_text):
    source_batches = source_text.split('.\n')
    target_batches = target_text.split('.\n')

    print("TEXT LENGTHS")
    print(len(source_text))
    print(len(target_text))

    source_batches_len = [len(batch) for batch in source_batches]
    target_batches_len = [len(batch) for batch in target_batches]

    print("HERE ARE BATCHES")
    print(sum(source_batches_len), len(source_batches), source_batches_len)
    print(sum(target_batches_len), len(target_batches), target_batches_len)

    new_source_batches = []
    new_target_batches = []

    i = 0
    j = 0

    while len(source_batches) > 0 and len(target_batches) > 0:
        new_source_batches.append(source_batches[0])
        del source_batches[0]
        new_target_batches.append(target_batches[0])
        del target_batches[0]

        if len(new_source_batches[i]) > len(new_target_batches[j]) + 0.2 * len(new_target_batches[j]):
            new_target_batches[j] = new_target_batches[j] + target_batches[0]
            del target_batches[0]
        else:
            i += 1
            j += 1


    print("HERE ARE NEW BATCHES")
    print([len(batch) for batch in new_source_batches])
    print([len(batch) for batch in new_target_batches])

    new_source_batches_len = [len(batch) for batch in new_source_batches]
    new_target_batches_len = [len(batch) for batch in new_target_batches]

    print("HERE ARE BATCHES")
    print(sum(new_source_batches_len), len(new_source_batches), new_source_batches_len)
    print(sum(new_target_batches_len), len(new_target_batches), new_target_batches_len)

    # print("SAVE TO FILE")
    # write_batches_to_file_as_list(source_batches, "source_batches.txt")
    # write_batches_to_file_as_list(target_batches, "target_batches.txt")

    return source_text, target_text