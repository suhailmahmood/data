"""
This module compares two versions of the text of a given Hadith.

External dependencies (pip package):
- BeautifulSoup
- lxml
"""
__author__ = 'Suhail Mahmood'
__version__ = '1.0'

import difflib
import re
import unicodedata
from bs4 import BeautifulSoup


class HadithDiffer:
    """
    A class to compare two versions of the text of a given Hadith.

    Usage:
    To compare ignoring the diacritics:
    similarity = HadithDiffer().set_hadith_texts(text1, text2).ignore_diacritics().compare()

    To compare without ignoring the diacritics:
    similarity = HadithDiffer().set_hadith_texts(text1, text2).ignore_diacritics(False).compare()
    Or,
    similarity = HadithDiffer().set_hadith_texts(text1, text2).compare()
    """
    _hadith_text1 = ''
    _hadith_text1_cleaned = ''
    _hadith_text2 = ''
    _hadith_text2_cleaned = ''
    _ignore_diacritics = False

    def set_hadith_texts(self, hadith_text1: str, hadith_text2: str):
        self._hadith_text1 = hadith_text1
        self._hadith_text1_cleaned = self._clean_up(self._hadith_text1)

        self._hadith_text2 = hadith_text2
        self._hadith_text2_cleaned = self._clean_up(self._hadith_text2)

        return self

    def ignore_diacritics(self, ignore: bool = True):
        self._ignore_diacritics = ignore
        return self

    def compare(self) -> float:
        """
        Compares the hadith texts set using setHadithTexts() and returns a value
        in the range 0 to 1 that indicates the similarity between the two texts.
        """
        if not self._hadith_text1 or not self._hadith_text2:
            raise Exception('Hadith texts to compare not set. Use setHadithTexts() to set the texts...')

        text1 = self._hadith_text1_cleaned
        text2 = self._hadith_text2_cleaned

        if self._ignore_diacritics:
            text1 = self._remove_diacritics(self._hadith_text1_cleaned)
            text2 = self._remove_diacritics(self._hadith_text2_cleaned)

        sm = difflib.SequenceMatcher(None, text1, text2)
        return sm.ratio()

    @staticmethod
    def _clean_up(hadith_text: str) -> str:
        """
        Cleans up the hadith text of any punctuation marks, removes multiple
        consecutive whitespaces, and removes any html markup.
        """
        punctuations = ''.join([
            # Collected from https://en.wikipedia.org/wiki/Arabic_script_in_Unicode#Punctuation_and_ornaments
            chr(int('060C', 16)),  # ARABIC COMMA
            chr(int('060D', 16)),  # ARABIC DATE SEPARATOR
            chr(int('060E', 16)),  # ARABIC POETIC VERSE SIGN
            chr(int('060F', 16)),  # ARABIC SIGN MISRA
            chr(int('061B', 16)),  # ARABIC SEMICOLON
            chr(int('061E', 16)),  # ARABIC TRIPLE DOT PUNCTUATION MARK
            chr(int('061F', 16)),  # ARABIC QUESTION MARK
            chr(int('066D', 16)),  # ARABIC FIVE POINTED STAR
            chr(int('06D4', 16)),  # ARABIC FULL STOP
            chr(int('06DD', 16)),  # ARABIC END OF AYAH
            chr(int('06DE', 16)),  # ARABIC START OF RUB EL HIZB
            chr(int('06E9', 16)),  # ARABIC PLACE OF SAJDAH
            chr(int('06FD', 16)),  # ARABIC SIGN SINDHI AMPERSAND
            chr(int('FD3E', 16)),  # Arabic ornate left parenthesis
            chr(int('FD3F', 16)),  # Arabic ornate right parenthesis
        ])

        # Removing punctuations
        cleaned_text = re.sub('[' + punctuations + ']', ' ', hadith_text)

        # Removing any html markup
        cleaned_text = BeautifulSoup(cleaned_text, 'lxml').text

        # Removing multiple consecutive whitespaces, including newlines
        cleaned_text = ' '.join(cleaned_text.split())

        return cleaned_text

    @staticmethod
    def _remove_diacritics(hadith_text: str) -> str:
        """
        Strips the hadith text of any diacritics.
        """
        # Decomposing characters with diacritics into their canonical decomposition
        normalized = unicodedata.normalize('NFD', hadith_text)

        # Removing diacritics
        diacritic_stripped = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')

        return diacritic_stripped
