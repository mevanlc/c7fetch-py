import typer

from . import config, fetch, review, search, typer_util

app = typer_util.TyperAlias(context_settings={"help_option_names": ["-h", "--help"]})
app.add_module(config)
app.add_module(search)
app.add_module(fetch)
app.add_module(review)

# @app.callback(invoke_without_command=True)
# ctx: typer.Context
def main():
    pass

if __name__ == "__main__":
    app()
