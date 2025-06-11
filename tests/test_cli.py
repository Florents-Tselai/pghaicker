from click.testing import CliRunner

from pghaicker.cli import cli
def test_summarize_cli_int_id():
    result = CliRunner().invoke(cli, ["summarize", "2626029"])
    assert result.exit_code == 0

def test_summarize_cli_url():
    result = CliRunner().invoke(cli, ["summarize", "https://www.postgresql.org/message-id/flat/CAApHDvrdxSwUt3sqhWMNnb_QwaX1A1TCuFWzCvirqKZo9aK_QQ%40mail.gmail.com"])
    assert result.exit_code == 0
