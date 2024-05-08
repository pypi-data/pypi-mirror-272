"""
@Date: 2024-05-06 20:40 

@Author: oceanumeric

@File: num2words_fr.py

Reference:

- https://github.com/GaspardPO/kata-number-to-french-converter

- https://github.com/Ballasi/num2words/blob/master/src/lang/fr.rs

- https://github.com/savoirfairelinux/num2words/blob/5e6fa94866eef0ea5b5df6843699c64379d02c81/num2words/lang_FR.py
"""

UNITS = [
    "zéro",
    "un",
    "deux",
    "trois",
    "quatre",
    "cinq",
    "six",
    "sept",
    "huit",
    "neuf",
    "dix",
    "onze",
    "douze",
    "treize",
    "quatorze",
    "quinze",
    "seize",
    "dix-sept",
    "dix-huit",
    "dix-neuf",
]
# Tens up to 60
TENS_BASE = {
    20: "vingt",
    30: "trente",
    40: "quarante",
    50: "cinquante",
    60: "soixante",
}

# Tens up to 80 for France
TENS_FR = {**TENS_BASE, 80: "quatre-vingt"}

# Tens up to 90 for Belgium
TENS_FR_BE = {**TENS_BASE, 70: "septante", 80: "huitante", 90: "nonante"}


class Num2Words:
    """A class to convert numbers to words in French.

    Attributes:
    -----------
    lang: str
        The language to use for conversion. Default is 'FR' for France.
        Can only be either 'FR' for France or 'BE' for Belgium.

    Methods:
    --------
    convert(num: int) -> str:
        Convert a number to words in French or Belgium.
    """

    def __init__(self, lang: str = "FR") -> None:
        """
        parameters:
        -----------
        lang: str
            The language to use for conversion. Default is 'FR' for France.
            Can only be either 'FR' for France or 'BE' for Belgium.

        Raises:
        -------
        ValueError: If the language is not 'FR' or 'BE'.
        """

        if lang not in ["FR", "BE"]:
            raise ValueError("Invalid language. Please choose either 'FR' or 'BE'.")

        self.lang = lang
        
    
    def convert(self, num: int) -> str:
        """
        Convert a number to words in French or Belgium.
        
        parameters:
        -----------
        num: int
            The number to convert to words.
        
        returns:
        --------
        str
            The number in words.
        """

        if not isinstance(num, int):
            raise ValueError("The number must be an integer.")

        assert num >= 0

        quotient, remainder = divmod(num, 1000)

        if quotient == 0:
            return self._convert_hundreds(remainder)
        else:
            if remainder == 0:
                if quotient == 1:
                    return "mille"
                return self._convert_hundreds(quotient, set_pluras=False) + "-milles"
            if quotient == 1:
                return "mille-" + self._convert_hundreds(remainder)
            return (
                self._convert_hundreds(quotient)
                + "-mille-"
                + self._convert_hundreds(remainder)
            )

    def _convert_20_to_99(self, num: int) -> str:
        """
        Convert a number between 20 and 99 to words. It only works for Belgium.
        """

        # assert 20 <= num <= 99
        assert 20 <= num <= 99

        quotient, remainder = divmod(num, 10)
        tenth_digit = quotient * 10

        if remainder == 0:
            return TENS_FR_BE[tenth_digit]
        else:
            if remainder == 1:
                return TENS_FR_BE[tenth_digit] + "-et-" + UNITS[remainder]
            else:
                return TENS_FR_BE[tenth_digit] + "-" + UNITS[remainder]

    def _convert_20_to_69(self, num: int) -> str:
        """
        Convert a number between 20 and 69 to words. It only works for France.
        """

        # assert 20 <= num <= 70
        assert 20 <= num < 70

        quotient, remainder = divmod(num, 10)
        tenth_digit = quotient * 10

        if remainder == 0:
            return TENS_FR[tenth_digit]
        else:
            if remainder == 1:
                return TENS_FR[tenth_digit] + "-et-" + UNITS[remainder]
            else:
                return TENS_FR[tenth_digit] + "-" + UNITS[remainder]

    def _convert_70_to_99(self, num: int, set_pluras: bool = True) -> str:
        """
        Convert a number between 70 and 99 to words. It only works for France.
        """

        # assert 70 <= num <= 99
        assert 70 <= num <= 99

        quotient, remainder = divmod(num, 20)
        tenth_digit = quotient * 20

        if remainder == 0:
            # it is 80
            if set_pluras:
                return TENS_FR[tenth_digit] + "s"
            return TENS_FR[tenth_digit]
        else:
            if num == 71:
                # 71 is a special case
                return TENS_FR[tenth_digit] + "-et-onze"
            return TENS_FR[tenth_digit] + "-" + UNITS[remainder]

    def _convert_tens(self, num: int, set_pluras: bool = True) -> str:
        """
        Convert a number between 0 and 99 to words.
        """

        assert 0 <= num <= 99

        if self.lang == "BE":
            if num < 20:
                return UNITS[num]
            else:
                return self._convert_20_to_99(num)

        if num < 20:
            return UNITS[num]
        elif num < 70:
            return self._convert_20_to_69(num)
        else:
            return self._convert_70_to_99(num, set_pluras=set_pluras)

    def _convert_hundreds(self, num: int, set_pluras: bool = True) -> str:
        """
        Convert a number between 0 and 999 to words.
        """

        assert 0 <= num <= 999

        quotient, remainder = divmod(num, 100)

        if quotient == 0:
            return self._convert_tens(remainder)
        else:
            if remainder == 0:
                if quotient == 1:
                    return "cent"
                if set_pluras:
                    return UNITS[quotient] + "-cents"
                return UNITS[quotient] + "-cent"
            if quotient == 1:
                return "cent-" + self._convert_tens(remainder, set_pluras=set_pluras)
            return (
                UNITS[quotient]
                + "-cent-"
                + self._convert_tens(remainder, set_pluras=set_pluras)
            )



if __name__ == "__main__":
    import random

    # simple test with random numbers
    print("Test for lang = 'BE'")
    foo = Num2Words(lang="BE")
    for x in range(10):
        num = random.randint(0, 999999)
        print(f"{num}: {foo.convert(num)}")

    print("-" * 50)
    print("Test for lang = 'FR'")
    foo = Num2Words(lang="FR")
    for x in range(10):
        num = random.randint(0, 999999)
        print(f"{num}: {foo.convert(num)}")
