import asyncio

import cpop.hub


def main():
    # Set the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Start the async code
    try:
        asyncio.run(amain(loop))
    finally:
        loop.close()


async def amain(loop):
    async with cpop.hub.Hub(cli="cli") as hub:
        await hub.log.debug("Initialized the hub")

        hold = asyncio.create_task(hub._holder())

        if "legacy" in hub.cli:
            await hub.cli.legacy.patch(loop=loop)

        try:
            # Start the hub cli
            await hub.cli.init.run()
        except KeyboardInterrupt:
            await hub.log.error("Caught keyboard interrupt.  Cancelling...")
        except SystemExit:
            ...
        finally:
            await hub.log.debug("Cleaning up")
            await hub._tasks.put(cpop.hub.SHUTDOWN_SIGNAL)
            await asyncio.sleep(0)
            if hold:
                await hold
            await loop.shutdown_asyncgens()


if __name__ == "__main__":
    main()
