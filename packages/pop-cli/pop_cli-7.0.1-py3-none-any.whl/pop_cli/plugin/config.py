async def override(hub, cli: str, opts: dict):
    """
    Parse the cli again using arguments not used up by pop-cli.
    Override hub.OPT with the new CLI options but maintain, config, os, and defaults parsed earlier

    Args:
        hub (pop.hub.Hub): The global namespace
        cli (str): The namespace to use as the authoritative cli
        opts (dict): Previously parsed hub.OPT
    """
    new_config = hub.lib.collections.defaultdict(dict)
    for namespace, data in opts.items():
        try:
            for k, v in data.items():
                if namespace == "pop" and k in ("subparser", "global_clis"):
                    continue

                new_config[namespace][k] = {"default": v}
        except AttributeError:
            continue

    # There is a user defined-cli, let it parse the remaining args it's own way
    hub._opt = await hub.pop.config.load(
        # Pass all remaining args onto the new parser
        cli=cli,
        parser_args=tuple(opts.cli.args),
        # Override the existing opts with new data from the next cli
        cli_config=hub._dynamic.config.cli_config,
        # Pass the already parsed opts as the new config
        config=new_config,
        subcommands=hub._dynamic.config.subcommands,
    )
