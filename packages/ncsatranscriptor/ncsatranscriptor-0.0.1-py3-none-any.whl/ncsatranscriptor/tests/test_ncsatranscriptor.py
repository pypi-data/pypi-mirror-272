import unittest
from unittest import TestCase

import ncsatranscriptor.ncsatranscriptor as ncsat

ncsaStringTranscriptor = ncsat.StringTranscriptor()


class TestStringTranscriptor(TestCase):
    def test_replace_vowels_by_alphabetical_index(self):
        input_string = '''National Center for Supercomputing Applications'''
        ncsaStringTranscriptor.initial_string = input_string
        transcribed_string = ncsaStringTranscriptor.run_transcription("basic")
        expected_outcome = "N1t915n1l C5nt5r f15r S21p5rc15mp21t9ng 1ppl9c1t915ns"
        if transcribed_string == expected_outcome:
            pass
        else:
            self.fail()

    def test_replace_vowels_by_alphabetical_index_repeats(self):
        input_string = '''Naational Ceeeenter for Suuupercomputing Appliiications'''
        ncsaStringTranscriptor.initial_string = input_string
        transcribed_string = ncsaStringTranscriptor.run_transcription("basic")
        expected_outcome = "N11t915n1l C5555nt5r f15r S212121p5rc15mp21t9ng 1ppl999c1t915ns"
        if transcribed_string == expected_outcome:
            pass
        else:
            self.fail()

    def test_replace_vowels_by_alphabetical_index_non_ascii(self):
        input_string = '''Na¶tional CeÆnter fo£r Supercomputing Applica©tions'''
        ncsaStringTranscriptor.initial_string = input_string
        transcribed_string = ncsaStringTranscriptor.run_transcription("basic")
        expected_outcome = "N1¶t915n1l C5Ænt5r f15£r S21p5rc15mp21t9ng 1ppl9c1©t915ns"
        if transcribed_string == expected_outcome:
            pass
        else:
            self.fail()

    def test_count_consonants(self):
        input_string = '''National Center for Supercomputing Applications'''
        count_of_consonants = ncsaStringTranscriptor.count_consonants(substrate_string=input_string)
        expected_outcome = 26
        if count_of_consonants == expected_outcome:
            pass
        else:
            self.fail()

    def test_count_consonants_non_alpha(self):
        input_string = '''National !!Center for Supercomputing Applications@#^@#%^'''
        count_of_consonants = ncsaStringTranscriptor.count_consonants(substrate_string=input_string)
        expected_outcome = 26
        if count_of_consonants == expected_outcome:
            pass
        else:
            self.fail()

    def test_count_consonants_non_ascii(self):
        input_string = '''Na¶tional CeÆnter fo£r Supercomputing Applica©tions'''
        count_of_consonants = ncsaStringTranscriptor.count_consonants(substrate_string=input_string)
        expected_outcome = 26
        if count_of_consonants == expected_outcome:
            pass
        else:
            self.fail()

    def test_get_english_vowels(self):
        these_english_vowels = ncsaStringTranscriptor.get_english_vowels()
        reference_list = ['a', 'e', 'i', 'o', 'u']
        if set(reference_list) == set(these_english_vowels):
            pass
        else:
            self.fail()


def main():
    unittest.main()


if __name__ == "__main__":
    main()