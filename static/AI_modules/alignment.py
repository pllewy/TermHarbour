# Author: Paweł Lewicki

from simalign import SentenceAligner

from static.text_batches import create_text_batches
from static.timer import measure_time
from static.AI_modules.extraction_01 import (post_process_terms, preprocess_text, load_spacy_model,
                                             extract_specialist_terms_with_patterns, combine_term_lists,
                                             extract_ner_terms)
@measure_time
def align(source_sentence, target_sentence, alignment_method="inter", print_output=False, print_input=False):
    """
    This function aligns a source sentence with a target sentence using a specified alignment method.

    Args:
        source_sentence (list): The source sentence to be aligned.
        target_sentence (list): The target sentence to be aligned.
        alignment_method (str, optional): The alignment method to be used. Defaults to "inter". Options: "mwmf", "inter", "itermax".
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


@measure_time
def extract_terms(input_text, lang, preprocessing=True):
    nlp = load_spacy_model(lang)
    if preprocessing:
        text_preprocessed = preprocess_text(input_text)
    else:
        text_preprocessed = input_text
    terms_ner = extract_ner_terms(input_text, nlp)
    terms_pattern = extract_specialist_terms_with_patterns(text_preprocessed, nlp)
    terms_pattern = post_process_terms(terms_pattern)
    return combine_term_lists(terms_pattern, terms_ner)


def full_alignment_process(source_text, target_text, source_lang, target_lang, batching_method="PARAGRAPH"):
    # Extract GLOBAL terms from text
    source_terms = extract_terms(source_text, source_lang)
    target_terms = extract_terms(target_text, target_lang)

    print("SOURCE TERMS:", len(source_terms))
    print("TARGET TERMS:", len(target_terms))

    result_term_list = []

    source_batches = []
    target_batches = []
    if batching_method == 'PARAGRAPH':
        # Create text batches for possibly faster simalign
        # returns list of words (for closer paragraph matching)
        source_batches, target_batches = create_text_batches(source_text, target_text)

        # check difference in number of batches. You need it to ensure you check adjacent batches in both languages
        no_batches_diff = abs(len(source_batches) - len(target_batches))

        iterator = min(len(source_batches), len(target_batches))
    else:
        iterator = 1

    for i in range(iterator):

        if batching_method == 'PARAGRAPH':
            curr_src_batch = source_batches[i]
            curr_tgt_batch = target_batches[i]
        else:
            curr_src_batch = preprocess_text(source_text).split(' ')
            curr_tgt_batch = preprocess_text(target_text).split(' ')

        print("\nLIST LENGTHS: ", len(curr_src_batch), len(curr_tgt_batch))
        alignment = align(curr_src_batch, curr_tgt_batch)

        source_batch_terms = extract_terms(' '.join(curr_src_batch), source_lang, preprocessing=False)
        target_batch_terms = extract_terms(' '.join(curr_tgt_batch), target_lang, preprocessing=False)

        print("SOURCE BATCH TERMS BY SEBA: ", len(source_batch_terms), source_batch_terms)
        print("TARGET BATCH TERMS BY SEBA: ", len(target_batch_terms), target_batch_terms)

        print("ALIGNMENT: ", len(alignment), alignment)

        tgt_little_terms = []
        # For each multi-word term in target batch
        for term in target_batch_terms:
            # Split it into words
            tgt_little_terms.append(term.split('_'))

        print("\nTARGET LITTLE TERMS: ", tgt_little_terms)

        # For each multi-word term in source batch
        for term in source_batch_terms:
            # Split it into words
            src_little_terms = term.split('_')

            print("\nSOURCE LITTLE TERMS: ", src_little_terms)
            match_result = []
            for l in range(len(tgt_little_terms)):
                match_result.append(0)

            # For each word in source term
            for little_term in src_little_terms:
                # Get all alignments of this word
                matching_tuples = [t[1] for t in alignment if t[0].lower() == little_term.lower()]
                # Remove duplicates
                matching_tuples = list(set(matching_tuples))
                print("MATCHING TUPLES: ", little_term, " ", matching_tuples)

                # Count matching words in tgt_little_terms
                match_scores = []

                for tgt_term in tgt_little_terms:
                    match_count = sum(1 for word in tgt_term if word in matching_tuples)
                    match_scores.append(match_count)
                # print("MATCH SCORES: ", little_term, " ", match_scores)

                for i in range(len(match_scores)):
                    if match_scores[i] > 0:
                        match_scores[i] = 1
                match_result = [x + y for x, y in zip(match_result, match_scores)]

            terms_result = []
            # Take each target term that has more than half of the words matched
            for k in range(len(tgt_little_terms)):
                # Another possible condition <= len(tgt_little_terms[k])
                if ((match_result[k] > (len(tgt_little_terms[k]) // 2)) &
                        (len(tgt_little_terms[k]) >= len(src_little_terms) // 2) &
                        (len(tgt_little_terms[k]) <= len(src_little_terms))):
                    terms_result.append(tgt_little_terms[k])

            if len(terms_result) > 0:
                result_term_list.append([term, terms_result])
            # print("MATCH RESULT: ", term, " ", match_result, " ", terms_result)

            print("RESULT TERM LIST: ", len(result_term_list))

    print("RESULT TERM LIST with duplicates: ", len(result_term_list))

    for i in range(len(result_term_list)):
        for j in range(i + 1, len(result_term_list)):
            if result_term_list[i][0] == result_term_list[j][0]:
                result_term_list[i][1] += result_term_list[j][1]
                result_term_list[j][1] = []

    result_term_list = [term for term in result_term_list if term[1]]

    for line in range(len(result_term_list)):
        result_set = []
        for sublist_index in range(len(result_term_list[line][1])):
            term = ""
            for word in range(len(result_term_list[line][1][sublist_index])):
                term = term + result_term_list[line][1][sublist_index][word] + " "
            result_set.append(term)
        result_term_list[line] = [result_term_list[line][0], list(set(result_set))]

    print("RESULT TERM LIST without duplicates: ", len(result_term_list))

    # print("\n\nRESULT TERM LIST: ", result_term_list)

    return result_term_list, source_terms, target_terms
