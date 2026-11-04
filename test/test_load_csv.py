import pytest

from card_game.LoadCSV import create_csv_reader


def test_create_csv_reader_invalid_path(capsys):
    with pytest.raises(IOError):
        create_csv_reader("does_not_exist.csv")

    captured = capsys.readouterr()
    assert "An error occurred." in captured.out


def test_create_csv_reader_valid_data(tmp_path):
    # Create a temporary CSV file
    csv_file = tmp_path / "cards.csv"
    csv_file.write_text("Suit,Value\n" "Hearts,10\n" "Spades,Ace\n" "Diamonds,7\n")

    # Read the CSV using the function under test
    rows = list(create_csv_reader(csv_file))

    # Verify exactly 3 card records were returned
    assert len(rows) == 3

    # Verify the contents match the CSV data in order
    assert rows[0]["Suit"] == "Hearts"
    assert rows[0]["Value"] == "10"

    assert rows[1]["Suit"] == "Spades"
    assert rows[1]["Value"] == "Ace"

    assert rows[2]["Suit"] == "Diamonds"
    assert rows[2]["Value"] == "7"
