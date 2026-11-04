import pytest

from card_game.LoadCSV import create_csv_reader


def test_create_csv_reader_invalid_path(capsys):
    with pytest.raises(IOError):
        create_csv_reader("does_not_exist.csv")

    captured = capsys.readouterr()
    assert "An error occurred." in captured.out
