import asyncio
from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    async with rtbnext( client= ClientIdentity(
        name= "python-sdk-test",
        version= "1.0.0",
        contact="https://pypi.org/project/rtbnext"
    ) ) as client:

        # get daily winner / loser
        mover = await client.mover.index.get()

        if ( latest := mover.latest ) is not None:
            snapshot = await latest.data()

            print( "Mover snapshot:", snapshot["date"] )
            print( "Today net worth winners:", snapshot["today"]["networth"]["winner"] )
            print( "Today percent losers:", snapshot["today"]["percent"]["loser"] )


asyncio.run( main() )
