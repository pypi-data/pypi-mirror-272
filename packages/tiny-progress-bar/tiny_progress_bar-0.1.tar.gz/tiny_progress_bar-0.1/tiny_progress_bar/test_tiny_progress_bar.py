import pytest
import re
from tiny_progress_bar import progress_bar as pb


class TestProgressBar:
    def test_range__PASS(self, capsys):
        # Setup
        array = range(0, 10)
        for _ in pb(array, 10):
            ...

        out, _ = capsys.readouterr()
        out = re.sub(r"[\x08]", "", out)  # remove carriage return characters

        answer = """[=>         ] 10.0%[==>        ] 20.0%[===>       ] 30.0%[====>      ] 40.0%[=====>     ] 50.0%[======>    ] 60.0%[=======>   ] 70.0%[========>  ] 80.0%[=========> ] 90.0%[==========>] 100.0%\n"""

        # Test
        assert out == answer

        # Clean up - None

    def test_range_count__PASS(self, capsys):
        # Setup
        array = range(0, 10)
        count = 0
        for i in pb(array, 10):
            count += i

        out, _ = capsys.readouterr()
        out = re.sub(r"[\x08]", "", out)  # remove carriage return characters

        answer = """[=>         ] 10.0%[==>        ] 20.0%[===>       ] 30.0%[====>      ] 40.0%[=====>     ] 50.0%[======>    ] 60.0%[=======>   ] 70.0%[========>  ] 80.0%[=========> ] 90.0%[==========>] 100.0%\n"""

        # Test
        assert out == answer
        assert count == sum(array)

        # Clean up - None

    def test_range_negative_numbers__PASS(self, capsys):
        # Setup
        array = range(-10, 10)
        count = 0
        for i in pb(array, 10):
            count += i

        out, _ = capsys.readouterr()
        out = re.sub(r"[\x08]", "", out)  # remove carriage return characters

        answer = """[>          ]  5.0%[=>         ] 10.0%[=>         ] 15.0%[==>        ] 20.0%[==>        ] 25.0%[===>       ] 30.0%[===>       ] 35.0%[====>      ] 40.0%[====>      ] 45.0%[=====>     ] 50.0%[=====>     ] 55.0%[======>    ] 60.0%[======>    ] 65.0%[=======>   ] 70.0%[=======>   ] 75.0%[========>  ] 80.0%[========>  ] 85.0%[=========> ] 90.0%[=========> ] 95.0%[==========>] 100.0%\n"""
        # Test
        assert out == answer
        assert count == sum(array)

        # Clean up - None

    def test_list__PASS(self, capsys):
        # Setup
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i in pb(array, 10):
            ...

        out, _ = capsys.readouterr()
        out = re.sub(r"[\x08]", "", out)  # remove carriage return characters

        answer = """[=>         ] 10.0%[==>        ] 20.0%[===>       ] 30.0%[====>      ] 40.0%[=====>     ] 50.0%[======>    ] 60.0%[=======>   ] 70.0%[========>  ] 80.0%[=========> ] 90.0%[==========>] 100.0%\n"""
        # Test
        assert out == answer

        # Clean up - None

    def test_dict__PASS(self, capsys):
        # Setup
        dict_obj = {
            1: "a",
            2: "b",
            "c": 3,
            "f": "d",
            "fish": True,
            "potato": "salad",
            True: False,
            0.2: 0.11,
            None: False,
            "s": "c",
            False: True,
        }
        for i in pb(dict_obj, 10):
            ...

        out, _ = capsys.readouterr()
        out = re.sub(r"[\x08]", "", out)  # remove carriage return characters

        answer = """[=>         ] 10.0%[==>        ] 20.0%[===>       ] 30.0%[====>      ] 40.0%[=====>     ] 50.0%[======>    ] 60.0%[=======>   ] 70.0%[========>  ] 80.0%[=========> ] 90.0%[==========>] 100.0%\n"""
        # Test
        assert out == answer

        # Clean up - None

    def test_not_an_array__FAIL(self):
        # Setup
        not_an_array = 312
        expected_err = "'array' is not iterable. Please supply an iterable such as a list, string, dictionary, etc."
        with pytest.raises(TypeError) as actual_err:
            for _ in pb(not_an_array):
                ...

        # Test
        assert str(actual_err.value) == expected_err

        # Clean up - None

    def test_invalid_minimum_bar_length__FAIL(self):
        # Setup
        array = [1, 2, 3]
        bar_length = 9
        expected_err = f"Parameter 'bar_length' = {bar_length}. It needs to be at least 10 characters."
        with pytest.raises(ValueError) as actual_err:
            for _ in pb(array, bar_length=bar_length):
                ...

        # Test
        assert str(actual_err.value) == expected_err

        # Clean up - None
