import re

import typer
import typer.core


class TyperAliasGroup(typer.core.TyperGroup):
    _CMD_SPLIT_P = re.compile(r" ?[,|] ?")

    def get_command(self, ctx, cmd_name):
        cmd_name = self._group_cmd_name(cmd_name)
        return super().get_command(ctx, cmd_name)

    def _group_cmd_name(self, default_name):
        for cmd in self.commands.values():
            name = cmd.name
            if name and default_name in self._CMD_SPLIT_P.split(name):
                return name
        return default_name


class TyperAlias(typer.Typer):
    def __init__(self, *args, **kwargs):
        cs = kwargs.setdefault("context_settings", {})
        cs["help_option_names"] = list(set(cs.get("help_option_names", [])) | {"-h", "--help"})
        modname = kwargs.pop("module", None)
        if modname and "name" not in kwargs:
            kwargs["name"] = modname.split(".")[-1]

        kwargs.setdefault("cls", TyperAliasGroup)
        kwargs.setdefault("no_args_is_help", True)
        super().__init__(*args, **kwargs)

    def add_module(self, module):
        app = getattr(module, "app", None)
        if app:
            self.add_typer(app)
        else:
            raise ValueError(f"Module {module} has no attribute 'app'")
