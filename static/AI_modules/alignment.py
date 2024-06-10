# Author: Paweł Lewicki

from simalign import SentenceAligner

from static.timer import measure_time


@measure_time
def align(source_sentence, target_sentence, alignment_method="mwmf", print_output=False, print_input=False):
    """
    This function aligns a source sentence with a target sentence using a specified alignment method.

    Args:
        source_sentence (list): The source sentence to be aligned.
        target_sentence (list): The target sentence to be aligned.
        alignment_method (str, optional): The alignment method to be used. Defaults to "itermax". Options: "mwmf", "inter", "itermax".
        print_output (bool, optional): If True, prints the full alignment dictionary. Defaults to False.
        print_input (bool, optional): If True, prints the source and target sentences. Defaults to False.

    Returns:
        list: A list of word pairs from the source and target sentences that are aligned.
    """
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
    """
    This function aligns a source sentence with a target sentence and returns the full alignment dictionary.

    Args:
        source_sentence (list): The source sentence to be aligned.
        target_sentence (list): The target sentence to be aligned.
        print_input (bool, optional): If True, prints the source and target sentences. Defaults to False.
        print_output (bool, optional): If True, prints the full alignment dictionary. Defaults to False.

    Returns:
        dict: The full alignment dictionary.
    """

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