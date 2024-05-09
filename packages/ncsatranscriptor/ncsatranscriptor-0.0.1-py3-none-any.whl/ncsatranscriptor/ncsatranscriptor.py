import logging
import sys
import string
# setup imports: base python convenience functions only - keep away from func's that execute the main challenge

logger = logging.getLogger("mainLogger")


class StringTranscriptor(object):
    """
    A fairly simple string-based transcriptor class. Accepts input string and provides simple validations. Enables
    one or more transcription approaches to satisfy requirements (see docs)

    Attributes
    ----------
    _initial_string : str
        The basic starting string for transcription

    _transcribed_string : str
        The transcribed string after processing through the selected method. Remains None until transcription is
        triggered

    _transcription_methods : dict
        lookup-style map relating user-selectable method names (e.g. 'basic') to class methods for executing
        transcription

    Methods
    -------
    replace_vowels_by_alphabetical_index()
        Applies a basic transcription method to change vowels to their numeric alphabetical index

    count_consonants(type='transcribed')
        method which will count the number of consonants in either the starting or transcribed string.

    """

    def __init__(self, initial_string=None, transcription_method=None):
        self._initial_string = initial_string
        self._transcribed_string = transcription_method
        self._transcription_methods = {
            'basic': 'replace_vowels_by_alphabetical_index'
        }
        # levenshtein distance would work; specify objective function and minimize
        ### you'd have to find absolute minima for each substitution to avoid a=1, o=15 issues
        ### would make this inefficient (obviously. also you need to pre-compute the outcome)
        # NOT hamming distance - strings are of unequal length
        # pythonic regex via str.sub()
        # specific index slices by exact match
        logger.info('Initialized NCSA Transcriptor successfully.')

    @staticmethod
    def get_english_vowels() -> list:
        """
        Parameters
        ----------

        Returns
        ----------
        List of vowels - namely a, e, i, o u

        Notes
        ----------
        This method treats the character 'y' as a consonant

        """
        return list("aeiou")

    @staticmethod
    def get_alphabetical_characters() -> list:
        """
        Parameters
        ----------

        Returns
        ----------
        integer value - number of consonants in the string

        Notes
        ----------
        enables future use of alternative alphabets, orderings, etc. based on ascii definitions

        """
        all_lowercase_english_letters = string.ascii_lowercase
        list_of_english_letters = list(all_lowercase_english_letters)
        return list_of_english_letters

    # getters and setters via decorators
    @property
    def transcribed_string(self) -> str:
        """transcribed string getter"""
        return self._transcribed_string

    @transcribed_string.setter
    def transcribed_string(self, this_string: str) -> None:
        """transcribed string getter"""
        self._transcribed_string = this_string
        logger.info(f'Transcribed string successfully set to \'{self._transcribed_string}\'.')

    @property
    def initial_string(self) -> str:
        """initial string getter"""
        return self._initial_string

    @initial_string.setter
    def initial_string(self, this_string: str) -> None:
        """initial string getter"""
        self._initial_string = this_string
        logger.info(f'Initial string successfully set to \'{self._initial_string}\'.')

    @property
    def transcription_methods(self) -> dict:
        """transcription_methods getter"""
        return self._transcription_methods

    @transcription_methods.setter
    def transcription_methods(self, this_string: str) -> None:
        """transcription_methods getter"""
        logger.error('Do not attempt to dynamically set the available transcription methods.')
        logger.info('Invalid attempt to dynamically define transcription methods. No action taken.')

    @transcription_methods.deleter
    def transcription_methods(self) -> None:
        """transcription_methods deleter"""
        logger.error('Do not attempt to delete the available transcription methods.')
        logger.info('Invalid attempt to delete transcription methods. No action taken.')

    def count_consonants(self, substrate_string: str) -> int:
        """
        Parameters
        ----------
        substrate_string : str
            string for which the count of consonants will be determined


        Returns
        ----------
        integer value - number of consonants in the string

        """

        listified_string = list(substrate_string)

        this_alphabetical_index = self.get_alphabetical_characters()
        vowels = self.get_english_vowels()

        total_consonants = 0
        for i, c in enumerate(listified_string):
            lower_c = c.lower()
            if lower_c not in vowels and lower_c in this_alphabetical_index:
                # avoid counting spaces
                # there are both more concise and faster ways to do this, but i'm not optimizing early!
                total_consonants += 1

        return total_consonants

    def get_allowed_transcription_methods(self) -> list:
        """
        Parameters
        ----------

        Returns
        ----------
        a list of string values, each being the key to the methods dictionary that allows a user to select that method.

        """
        allowed_methods = [*self.transcription_methods.keys()]
        return allowed_methods

    def run_transcription(self, method_name) -> str:
        """
        Public method that enables calling of the transcription itself. Masks private method for transcription method
        dispatch

        Parameters
        ----------
        method_name : str
            One of the acceptable method names contained in this package; defined by object initiation

        Returns
        ----------
        transcribed_string : str
            Actual outputs from this package: the updated string with the specified transcription completed

        """
        return self._method_dispatch(method_name)

    def _method_dispatch(self, method_name) -> str:
        """
        Simple method dispatch based on method name; executes actual calling and returning of method results.

        Parameters
        ----------
        method_name : str
            One of the acceptable method names contained in this package; defined by object initiation

        Returns
        ----------
        transcribed_string : str
            Actual outputs from this package: the updated string with the specified transcription completed

        """
        transcribed_string = None
        try:
            current_transcription_methods = self.transcription_methods
            if method_name in current_transcription_methods.keys():
                transcription_function_name = current_transcription_methods.get(method_name, None)
                if transcription_function_name is None:
                    logger.error("Accessed a transcription method which is not a function")
                    raise ValueError

            else:
                logger.error("Attempted to access transcription method which does not exist")
                raise KeyError

            transcription_function = getattr(self, transcription_function_name)
            transcribed_string = transcription_function()
            if transcribed_string is not None:
                return transcribed_string

            else:
                logger.error("Something has gone wrong in string transcription.")
                raise ValueError

        except ValueError as e:
            logger.error(f"string before transcription: {str(self.initial_string)}")
            logger.error(f"string after transcription: {str(transcribed_string)}")
            logger.error(e)
            logger.error("Exiting.")
            sys.exit(1)
        except KeyError as e:
            logger.error("Likely malformed method name in transcription execution")
            logger.error(f"name: {method_name}")
            logger.error("Exiting.")
            sys.exit(1)

    def replace_vowels_by_alphabetical_index(self) -> str:
        """
        Parameters
        ----------

        Returns
        ----------
        string with each vowel replaces with its numeric position in english alphabetical sort
        """
        starting_string = self.initial_string
        starting_string_list = list(starting_string)
        vowels = self.get_english_vowels()
        # we're going to say Y is not a vowel.
        # fortunately, the target string doesn't have any Ys, but other words do!
        # I have no desire to get into classification of each Y-containing english word as using the Y character as
        # vowel/not-vowel
        # vowel is a weird word.
        this_alphabetical_index = self.get_alphabetical_characters()

        # there are faster, more concise ways, but again, optimize late.
        for i, c in enumerate(starting_string):
            lower_c = c.lower()
            if lower_c in vowels:
                starting_string_list[i] = str(this_alphabetical_index.index(lower_c) + 1)

        self.transcribed_string = "".join(starting_string_list)
        return self.transcribed_string
