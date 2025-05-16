from click.testing import CliRunner

from pghaicker.cli import cli
def test_summarize_cli():
    result = CliRunner().invoke(cli, ["summarize", "2626029"])
    assert result.exit_code == 0