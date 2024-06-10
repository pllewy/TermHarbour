from static.AI_modules.extraction_01 import preprocess_text
from static.timer import measure_time


def write_batches_to_file_as_list(batches, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("[\n")
        for batch in batches:
            file.write(f"    {repr(batch)},\n")
        file.write("]\n")


@measure_time
def create_text_batches(raw_src_text, raw_tgt_text, save_to_file=False):
    src_batches = raw_src_text.split('.\n')
    tgt_batches = raw_tgt_text.split('.\n')

    print("\n\nTEXT LENGTHS")
    print(len(raw_src_text))
    print(len(raw_tgt_text))

    for i in range(len(src_batches)):
        src_batches[i] = preprocess_text(src_batches[i])
        src_batches[i] = src_batches[i].split(' ')

    for i in range(len(tgt_batches)):
        tgt_batches[i] = preprocess_text(tgt_batches[i])
        tgt_batches[i] = tgt_batches[i].split(' ')

    src_batches_len = [len(batch) for batch in src_batches]
    tgt_batches_len = [len(batch) for batch in tgt_batches]

    print("\nHERE ARE BATCHES")
    print(sum(src_batches_len), len(src_batches), src_batches_len)
    print(sum(tgt_batches_len), len(tgt_batches), tgt_batches_len)

    new_src_batches = []
    new_tgt_batches = []

    i = 0
    j = 0

    # Initialize the new batches
    new_src_batches.append(src_batches[0])
    del src_batches[0]
    new_tgt_batches.append(tgt_batches[0])
    del tgt_batches[0]

    while len(src_batches) > 0 and len(tgt_batches) > 0:
        # PRINTER
        src_batches_len = [len(batch) for batch in src_batches]
        tgt_batches_len = [len(batch) for batch in tgt_batches]
        new_src_batches_len = [len(batch) for batch in new_src_batches]
        new_tgt_batches_len = [len(batch) for batch in new_tgt_batches]

        print("\nHERE ARE BATCHES in while loop")
        print("old src: ", sum(src_batches_len), len(src_batches), src_batches_len)
        print("old tgt: ", sum(tgt_batches_len), len(tgt_batches), tgt_batches_len)
        print("new src: ", sum(new_src_batches_len), len(new_src_batches), new_src_batches_len)
        print("new tgt: ", sum(new_tgt_batches_len), len(new_tgt_batches), new_tgt_batches_len)
        # END PRINTER

        if len(new_src_batches[i]) > len(new_tgt_batches[j]) + 0.3 * len(new_tgt_batches[j]):
            print("MERGING TGT")
            new_tgt_batches[j] = new_tgt_batches[j] + tgt_batches[0]
            del tgt_batches[0]
        else:
            i += 1
            j += 1
            new_src_batches.append(src_batches[0])
            del src_batches[0]
            new_tgt_batches.append(tgt_batches[0])
            del tgt_batches[0]

    new_src_batches_len = [len(batch) for batch in new_src_batches]
    new_tgt_batches_len = [len(batch) for batch in new_tgt_batches]

    print("\nHERE ARE NEWER BATCHES")
    print(sum(new_src_batches_len), len(new_src_batches), new_src_batches_len)
    print(sum(new_tgt_batches_len), len(new_tgt_batches), new_tgt_batches_len)

    for i in range(len(src_batches)):
        new_src_batches.append(src_batches[i])

    for i in range(len(tgt_batches)):
        new_tgt_batches.append(tgt_batches[i])

    new_src_batches_len = [len(batch) for batch in new_src_batches]
    new_tgt_batches_len = [len(batch) for batch in new_tgt_batches]

    print("\nHERE ARE NEW BATCHES")
    print(sum(new_src_batches_len), len(new_src_batches), new_src_batches_len)
    print(sum(new_tgt_batches_len), len(new_tgt_batches), new_tgt_batches_len)
    print("\n\n")

    if save_to_file:
        print("SAVE TO FILE")
        write_batches_to_file_as_list(new_src_batches, "src_batches.txt")
        write_batches_to_file_as_list(new_tgt_batches, "tgt_batches.txt")

    return new_src_batches, new_tgt_batches
