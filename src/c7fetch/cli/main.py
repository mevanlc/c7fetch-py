from . import config, fetch, review, search, typer_util

app = typer_util.TyperAlias()
app.add_module(config)
app.add_module(search)
app.add_module(fetch)
app.add_module(review)


def main():
    app()


if __name__ == "__main__":
    app()
