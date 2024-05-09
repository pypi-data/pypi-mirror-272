CONFIG_KEYWORDS = (
    "os",
    "default",
)


async def load(
    hub,
    cli: str = None,
    cli_config: dict[str, object] = None,
    config: dict[str, object] = None,
    subcommands: dict[str, object] = None,
    global_clis: list[str] = None,
    parser_args: tuple = None,
):
    """
    Use the pop-config system to load up a fresh configuration for this project
    from the included conf.py file.
    """
    if cli_config is None:
        cli_config = hub._dynamic.config.get("cli_config") or {}

    # Get the plain config data that will tell us about OS vars and defaults
    if config is None:
        config = hub._dynamic.config.get("config") or {}

    # Merge config and cli_config
    full_config = hub.lib.cpop.data.update(cli_config, config, merge_lists=True)

    # These CLI namespaces will be added on top of any cli
    if global_clis is None:
        global_clis = ["log", "pop"]

    # Initialize the active cli, this is what will go into argparse
    active_cli = {}

    # Logging options and config file are part of the global namespace
    for gn in global_clis:
        active_cli.update(full_config.get(gn, {}).copy())

    if subcommands is None:
        subcommands = hub._dynamic.config.get("subcommands") or {}
    else:
        active_subcommands = subcommands

    active_subcommands = subcommands.get(cli, {})

    # Grab the named cli last so that it can override globals
    active_cli.update(full_config.get(cli, {}))

    # Add all the cli options to argparse and call hte parser
    cli_opts = await hub.pop.config.parse_cli(
        cli=cli,
        active_cli=active_cli,
        subcommands=active_subcommands,
        parser_args=parser_args,
    )

    # Load the config file parameter in the proper order
    pop_config = full_config.get("pop", {}).get("config") or {}
    config_file = (
        cli_opts.get("config")
        or hub.lib.os.environ.get("POP_CONFIG", pop_config.get("os"))
        # TODO let the "default" be a reference to a function that returns the default or add a key for default_ref
        or pop_config.get("default")
    )

    config_data = {}
    if config_file:
        config_file = hub.lib.aiopath.Path(config_file)
        if await config_file.exists():
            async with config_file.open("r") as fh:
                config_data = hub.lib.yaml.safe_load(await fh.read())

    opt = await hub.pop.config.prioritize(
        cli=cli,
        cli_opts=cli_opts,
        config=full_config,
        config_file_data=config_data,
        global_clis=global_clis,
    )

    return hub.lib.cpop.data.freeze(opt)


async def parse_cli(
    hub,
    cli: str,
    active_cli: dict[str, object],
    subcommands: dict[str, object],
    parser_args: tuple = None,
) -> dict[str, object]:
    """
    Create a parser and parse all the CLI options.

    Args:
        hub: The POP hub instance.
        cli (str): The name of the CLI being parsed.
        active_cli (dict): The active CLI configuration.
        subcommands (dict): The subcommands configuration.

    Returns:
        argparse.Namespace: The parsed CLI options.
    """
    if not cli:
        return {}

    # Create the main parser for the CLI
    parser = hub.lib.argparse.ArgumentParser(
        description=f"{cli.title().replace('_', ' ')} CLI Parser"
    )
    sparser = None
    subparsers = {}

    # Add subcommands to the parser
    for subcommand, opts in subcommands.items():
        if sparser is None:
            sparser = parser.add_subparsers(dest="SUBPARSER")
        if "description" not in opts:
            opts["description"] = (
                f"{cli.title().replace('_', ' ')} {subcommand.title().replace('_', ' ')} CLI Parser"
            )

        subparsers[subcommand] = sparser.add_parser(
            subcommand,
            **opts,
        )

    # Add CLI options to the parser
    groups = {}
    subparser_groups = {subcommand: {} for subcommand in subparsers}

    for name, namespace_opts in active_cli.items():
        opts = namespace_opts.copy()
        positional = opts.pop("positional", False)
        # Config keywords will be handled by "prioritize"
        for opt in CONFIG_KEYWORDS:
            opts.pop(opt, None)
        cli_name = name if positional else f"--{name.lower().replace('_', '-')}"

        choices = opts.pop("choices", ())
        if isinstance(choices, str):
            finder = hub
            for part in choices.split("."):
                finder = getattr(finder, part)

            opts["choices"] = list(finder)

        type_ = opts.pop("type", None)
        if type_:
            opts["type"] = eval(type_)

        options = opts.pop("options", ())
        arg_subparsers = opts.pop("subcommands", [])

        # Handle argument groups for top-level parser
        group_name = opts.pop("group", None)
        target_group = (
            groups.setdefault(group_name, parser.add_argument_group(group_name))
            if group_name
            else parser
        )
        if "__global__" in arg_subparsers or not arg_subparsers:
            target_group.add_argument(cli_name, *options, **opts)

        # Handle argument groups for subparsers
        for subcommand in arg_subparsers:
            if subcommand == "__global__":
                for subcmd, sparser in subparsers.items():
                    subparser_group = (
                        subparser_groups[subcmd].setdefault(
                            group_name, sparser.add_argument_group(group_name)
                        )
                        if group_name
                        else sparser
                    )
                    subparser_group.add_argument(cli_name, *options, **opts)
            elif subcommand in subparsers:
                subcmd = subcommand
                sparser = subparsers[subcommand]
                subparser_group = (
                    subparser_groups[subcmd].setdefault(
                        group_name, sparser.add_argument_group(group_name)
                    )
                    if group_name
                    else sparser
                )
                subparser_group.add_argument(cli_name, *options, **opts)

    return hub.lib.cpop.data.NamespaceDict(parser.parse_args(args=parser_args).__dict__)


PLACEHOLDER = object()


async def prioritize(
    hub,
    cli: str,
    cli_opts: dict[str, any],
    config: dict[str, any],
    config_file_data: dict[str, any],
    global_clis: list[str],
):
    """
    Prioritize configuration data from various sources.

    The order of priority is:
    1. CLI options (highest priority)
    2. Configuration file data
    3. OS environment variables
    4. Default values (lowest priority)
    5. Rewrite the root_dir option so running apps automatically changes dirs to user preferences

    Args:
        hub: The cpop.hub instance.
        cli (str): The name of the CLI being prioritized.
        cli_opts (dict): The parsed CLI options.
        config (dict): The configuration dictionary.
        config_file_data (dict): The data from the configuration file.

    Returns:
       cpop.data.ImmutableNamespaceDict: The prioritized configuration options.
    """
    opt = hub.lib.collections.defaultdict(dict)
    root_dir = None
    for namespace, args in config.items():
        for arg, data in args.items():
            # Initialize value to None
            value = None

            # 1. Check CLI options first
            if (namespace == cli or namespace in global_clis) and arg in cli_opts:
                value = cli_opts.get(arg)

            # 2. Check config file data if CLI option is not set
            if value is None:
                value = config_file_data.get(namespace, {}).get(arg, PLACEHOLDER)

            # Skip malformed config
            if not isinstance(data, dict):
                msg = f"Invalid data from config.yaml: {data}"
                raise TypeError(msg)

            # 3. Check OS environment variables if config file data is not set
            if value is PLACEHOLDER and "os" in data:
                value = hub.lib.os.environ.get(data["os"], PLACEHOLDER)

            # 4. Use default value if none of the above are set
            if value is PLACEHOLDER:
                value = data.get("default")
            if arg == "root_dir":
                root_dir = value
            # Set the value in the OPT dictionary
            opt[namespace][arg] = value
    await hub.pop.config.manage_paths(cli, opt, root_dir)

    opt["pop"]["subparser"] = cli_opts.get("SUBPARSER", "")
    opt["pop"]["global_clis"] = global_clis

    return hub.lib.cpop.data.freeze(opt)


async def manage_paths(hub, cli: str, opt: dict, root_dir: str):
    """
    If a root_dir has been specified, then we support rewriting roots,
    find all of the options for _dir, _path, and _file and update them
    """
    reroot = True if root_dir else False
    if not root_dir:
        root_dir = hub.lib.aiopath.Path(hub.lib.os.sep)
    if root_dir == hub.lib.os.sep:
        if hasattr(hub.lib.os, "geteuid") and hub.lib.os.geteuid() != 0 and reroot:
            # Using aiopath.Path on all paths makes testing on multiple OSes much easier.
            # Since we can just patch aiopath.Path to be aiopath.PureWindowsPath or aiopath.PurePosixPath
            root_dir = (await hub.lib.aiopath.Path("~").expanduser()) / f".{cli}"
        else:
            root_dir = hub.lib.aiopath.Path(root_dir)
    else:
        return

    for namespace, args in opt.items():
        for key, val in args.items():
            if key == "root_dir":
                opt[namespace][key] = str(root_dir)
                continue
            try:
                path = hub.lib.aiopath.Path(val)
                if (
                    key.endswith(("_dir", "_path", "_file"))
                    and await path.is_absolute()
                ):
                    # only update absolute paths for keys
                    #  ending in _dir, _path or _file
                    if await path.is_absolute():
                        # remove the root from the path, then join it to the main root
                        opt[namespace][key] = root_dir.joinpath(*path.parts[1:])
            except TypeError:
                continue
