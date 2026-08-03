import asyncio
from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    async with rtbnext( client= ClientIdentity(
        name= "python-sdk-test",
        version= "1.0.0",
        contact="https://pypi.org/project/rtbnext"
    ) ) as client:

        # list available lists
        lists = await client.list.index.collection()
        print( "Available lists:", lists.count )

        for list in lists:
            print( list.raw["name"], list.raw["uri"] )

        # access list snapshots
        if ( billionaires := lists.find( "billionaires" ) ) is not None:
            dates = await billionaires.dates.get()
            if ( latest := dates.year( 2026 ).latest ) is not None:
                snapshot = await latest.collection()
                print( "Latest Snapshot:", snapshot.count )

                for item in snapshot.take( 10 ):
                    print( item.raw["name"], item.raw["rank"] )


asyncio.run( main() )
