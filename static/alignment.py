from simalign import SentenceAligner


def align(source_sentence, target_sentence, alignment_method="itermax", print_output=False, print_input=False):
    # Initialize the sentence aligner
    aligner = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")

    # Perform alignment
    alignments = aligner.get_word_aligns(source_sentence, target_sentence)

    if print_input:
        print("Source Sentence: ", source_sentence)
        print("Target Sentence: ", target_sentence)

    if print_output:
        print("\nFull alignment dictionary:")
        print(alignments)

    alignments_table = []

    # mwmf, inter, itermax
    for align in alignments[alignment_method]:
        alignments_table.append([source_sentence[align[0]], target_sentence[align[1]]])

    return alignments_table

def align_sentences(source_sentence, target_sentence, print_input=False, print_output=False):
    # Initialize the sentence aligner
    aligner = SentenceAligner(model="bert", token_type="bpe", matching_methods="mai")

    # Perform alignment
    alignments = aligner.get_word_aligns(source_sentence, target_sentence)

    if print_input:
        print("Source Sentence: ", source_sentence)
        print("Target Sentence: ", target_sentence)

    if print_output:
        print("\nFull alignment dictionary:")
        print(alignments)



    return alignments