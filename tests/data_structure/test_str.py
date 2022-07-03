# Built-in/Generic Imports
import pytest

# Local Functions
from ictoolkit.data_structure.str import (
    list_to_str,
    find_longest_common_substring,
    clean_non_word_characters,
    remove_section,
)


__author__ = "IncognitoCoding"
__copyright__ = "Copyright 2022, test_str"
__credits__ = ["IncognitoCoding"]
__license__ = "MIT"
__version__ = "0.3"
__maintainer__ = "IncognitoCoding"
__status__ = "Production"


# ############################################################
# ######Section Test Part 1 (Successful Value Checking)#######
# ############################################################


def test_1_list_to_str():
    """
    This function tests converting a list to str.
    """
    my_str = list_to_str(value="sample1")
    assert "sample1" == my_str


def test_1_1_list_to_str():
    """
    This function tests converting a list to str.
    """
    my_str = list_to_str(value=["sample1", "sample2"])
    assert "sample1 sample2" == my_str


def test_1_2_list_to_str():
    """
    This function tests converting a list to str.
    """
    my_str = list_to_str(value=["sample1", "sample2"], sep=", ")
    assert "sample1, sample2" == my_str


def test_1_3_list_to_str():
    """
    This function tests converting a list to str.
    """
    my_str = list_to_str(value=["sample1", 2], sep=", ")
    assert "sample1, 2" == my_str


def test_1_find_longest_common_substring():
    """Tests getting a common substring"""
    common_substring = find_longest_common_substring("mysamplechangeshere", "mysampleneverchanges")
    assert "mysample" == common_substring


def test_1_clean_non_word_characters():
    """Tests cleaning non-word characters."""
    cleaned_string = clean_non_word_characters("BT-NNAK\x06")
    assert "BT-NNAK" == cleaned_string


def test_1_1_clean_non_word_characters():
    """Tests cleaning word characters. The original value should return with no change."""
    cleaned_string = clean_non_word_characters("BT-NNAK")
    assert "BT-NNAK" == cleaned_string


def test_1_remove_section():
    """
    This function tests removing the domain from the string.
    """
    my_value: str = "mydevice.sample.org"
    removal_values: tuple[str, ...] = ("badsample.org", "sample.org")
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=".")
    assert "mydevice" == stripped_value


def test_1_2_remove_section():
    """
    This function tests removing the folder path from the string with 100% match.
    """
    my_value: str = "C:\\Windows\\Temp\\myprogram"
    removal_values: tuple[str, ...] = ("Temp\\myprogram", "Temp\\myprogram1", "Temp\\myprogram2")
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep="\\", percent=80)
    assert "C:\\Windows" == stripped_value


def test_1_3_remove_section():
    """
    This function tests removing the folder path from the string with 90% match.
    """
    my_value: str = "C:\\Windows\\Temp\\myprogram"
    removal_values: tuple[str, ...] = ("Temp\\myprogram1", "Temp\\myprogram2")
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep="\\", percent=80)
    assert "C:\\Windows" == stripped_value


def test_1_4_remove_section():
    """
    This function tests the domain not matching any name at 100% match.

    The original value will return.
    """
    # my_value: str = "mydevice.sample.org"
    my_value: str = "aaaa.abc1.ds3a.d3gs"
    removal_values: tuple[str, ...] = ("badsample.org", "sample.o1rg")
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=".")
    assert "aaaa.abc1.ds3a.d3gs" == stripped_value


def test_1_5_remove_section(caplog):
    """
    This function tests the domain not matching any name at 100% match.

    The original value will return with a warning.
    """
    # my_value: str = "mydevice.sample.org"
    my_value: str = "aaaa.abc1.ds3a.d3gs"
    removal_values: tuple[str, ...] = ("badsample.org", "sample.o1rg")
    # Tests user warning.
    with pytest.warns(UserWarning):
        stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=".", percent=50)
    assert (
        "The processing orig_value (aaaa.abc1.ds3a.d3gs) contains a '.' but has no removal_value(s) match"
    ) in caplog.text
    assert "removal_values = badsample.org, sample.o1rg" in caplog.text
    assert (
        "If some orig_value entries have the potential to not match, please verify the orig_value is a value needing to be stripped."
    ) in caplog.text
    assert "aaaa.abc1.ds3a.d3gs" == stripped_value


def test_1_6_remove_section():
    """
    This function tests the value not matching an empty tuple.
    """
    my_value: str = "mydevice.sample.org"
    removal_values: tuple[str, ...] = ()
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=".")
    assert "mydevice.sample.org" == stripped_value


def test_1_7_remove_section():
    """
    This function tests two data sets.
    \t\\- 1st: The domain names with sub-domains is sorted by the sub-domains first,\\
    followed by the main domain.
    \t\\- 2nd: Removing the domain from the string based on the sorted domain names.
    """
    my_value: str = "mydevice.sim.redcolor.org"
    removal_values: tuple[str, ...] = (
        "sample.org",
        "home.sample.org",
        "redcolor.org",
        "home.redcolor.org",
        "sim.redcolor.org",
        "amp.redcolor.org",
    )
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=".")
    assert "mydevice" == stripped_value


def test_1_8_remove_section():
    """
    Tests a percent domain name match/strip.
    """
    # my_value: str = "mydevice.sim.randombluerandom"
    my_value: str = "mydevice.sim.randombluerandom"
    removal_values: str = "sim.randombluerandomredrandomgreen.org"
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=".", percent=45)
    assert "mydevice" == stripped_value


def test_1_9_remove_section():
    """
    Tests removal value with a dot separator and percent disabled.

    No match should be found.
    """
    # my_value: str = "mydevice.sim.randombluerandom"
    my_value: str = "mydevice.sim.randombluerandom"
    removal_values: tuple[str, ...] = ("randombluerandomredrandomgreen", "Sample")
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=".")
    assert my_value == stripped_value


def test_1_10_remove_section():
    """
    Tests removal value with a dot separator and percent enabled.
    """
    # my_value: str = "mydevice.sim.randombluerandom"
    my_value: str = "mydevice.sim.randombluerandom"
    removal_values: str = "randombluerandomredrandomgreen"
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=".", percent=40)
    assert "mydevice.sim" == stripped_value


def test_1_11_remove_section():
    """
    Tests removal values with a blank space separator.
    """
    my_value: str = "can you find me"
    removal_values: tuple[str, ...] = (
        "smith" "red",
        "blue",
        "home red",
        "sim blue",
        "find",
    )
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=" ", percent=50)
    assert "can you" == stripped_value


def test_1_12_remove_section():
    """
    Tests removal value with a dot separator with 99% match.

    This will return the original string because the match will be too high.
    """
    # my_value: str = "mydevice.sim.randombluerandom"
    my_value: str = "mydevice.sim.randombluerandom"
    removal_values: str = "randombluerandomredrandomgreen"
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep=".", percent=99)
    assert "mydevice.sim.randombluerandom" == stripped_value


def test_1_13_remove_section():
    """
    Tests removal value with a dash separator and no dashes in the orig_value.

    This will return the original string.
    """
    # my_value: str = "mydevice.sim.randombluerandom"
    my_value: str = "mydevice.sim.randombluerandom"
    removal_values: str = "randombluerandomredrandomgreen"
    stripped_value = remove_section(orig_value=my_value, removal_values=removal_values, sep="-")
    assert "mydevice.sim.randombluerandom" == stripped_value


# ############################################################
# ######Section Test Part 2 (Error/Catch Value Checking)######
# ############################################################


def test_2_find_longest_common_substring():
    """
    Tests sending an invalid string1 string type.
    """
    with pytest.raises(Exception) as excinfo:
        find_longest_common_substring(string1={"invalid Type"}, string2="mysamplechangeshere")
    assert (
        """The object value '{'invalid Type'}' is not an instance of the required class(es) or subclass(es)."""
        in str(excinfo.value)
    )
    assert """<class 'str'>""" in str(excinfo.value)
    assert """<class 'set'>""" in str(excinfo.value)


def test_2_1_find_longest_common_substring():
    """
    Tests sending an invalid string2 string type.
    """
    with pytest.raises(Exception) as excinfo:
        find_longest_common_substring(string1="mysamplechangeshere", string2={"invalid Type"})
    assert (
        """The object value '{'invalid Type'}' is not an instance of the required class(es) or subclass(es)."""
        in str(excinfo.value)
    )
    assert """<class 'str'>""" in str(excinfo.value)
    assert """<class 'set'>""" in str(excinfo.value)


def test_2_clean_non_word_characters():
    """
    Tests sending an invalid string2 string type.
    """
    with pytest.raises(Exception) as excinfo:
        clean_non_word_characters(string={"invalid Type"})
    assert (
        """The object value '{'invalid Type'}' is not an instance of the required class(es) or subclass(es)."""
        in str(excinfo.value)
    )
    assert """<class 'str'>""" in str(excinfo.value)
    assert """<class 'set'>""" in str(excinfo.value)


def test_2_remove_section():
    """
    Tests sending an invalid orig_value string type.
    """
    with pytest.raises(Exception) as excinfo:
        remove_section(orig_value={"invalid Type"}, removal_values=[""], sep=" ")
    assert (
        """The object value '{'invalid Type'}' is not an instance of the required class(es) or subclass(es)."""
        in str(excinfo.value)
    )
    assert """<class 'str'>""" in str(excinfo.value)
    assert """<class 'set'>""" in str(excinfo.value)


def test_2_1_remove_section():
    """
    Tests sending an invalid removal_values tuple type.
    """
    with pytest.raises(Exception) as excinfo:
        remove_section(orig_value="sampleswitch", removal_values={"invalid Type"}, sep=" ")
    assert (
        """The object value '{'invalid Type'}' is not an instance of the required class(es) or subclass(es)."""
        in str(excinfo.value)
    )
    assert """<class 'str'> | <class 'tuple'>""" in str(excinfo.value)
    assert """<class 'set'>""" in str(excinfo.value)


def test_2_2_remove_section():
    """
    Tests sending an invalid removal_values tuple value type.
    """
    with pytest.raises(Exception) as excinfo:
        remove_section(orig_value="sampleswitch", removal_values=({"invalid Type"}, {"invalid Type"}), sep=" ")
    assert """Invalid tuple value type. The removal_values arg requires a tuple of strings.""" in str(excinfo.value)
    assert """<class 'str'>""" in str(excinfo.value)
    assert """<class 'set'>""" in str(excinfo.value)


def test_2_3_remove_section():
    """
    Tests sending an invalid sep string type.
    """
    """
    Tests sending an invalid sep string type.
    """
    with pytest.raises(Exception) as excinfo:
        remove_section(orig_value="sampleswitch", removal_values="sample", sep="")
    assert """The value '' sent is not an accepted input.""" in str(excinfo.value)
    assert """Any value other than None or an empty string""" in str(excinfo.value)
    assert """<class 'str'>""" in str(excinfo.value)


def test_2_4_remove_section():
    """
    Tests sending an invalid sep string type.
    """
    with pytest.raises(Exception) as excinfo:
        remove_section(orig_value="sampleswitch", removal_values="sample", sep={"invalid Type"})
    assert (
        """The object value '{'invalid Type'}' is not an instance of the required class(es) or subclass(es)."""
        in str(excinfo.value)
    )
    assert """<class 'str'>""" in str(excinfo.value)
    assert """<class 'set'>""" in str(excinfo.value)


def test_2_5_remove_section():
    """
    Tests sending an invalid sep string type.
    """
    with pytest.raises(Exception) as excinfo:
        remove_section(orig_value="sampleswitch", removal_values="sample", sep=" ", percent={"invalid Type"})
    assert (
        """The object value '{'invalid Type'}' is not an instance of the required class(es) or subclass(es)."""
        in str(excinfo.value)
    )
    assert """<class 'int'>""" in str(excinfo.value)
    assert """<class 'set'>""" in str(excinfo.value)
