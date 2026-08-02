import asyncio

from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    client = rtbnext(
        client= ClientIdentity(
            name= "python-sdk-test",
            version= "1.0.0b1"
        )
    )

    lists = await client.list.index.collection()
    if ( list := lists.find( "rtb" ) ) is not None:
        dates = await list.dates.get()
        if ( snapshot := dates.first ) is not None:
            print( ( await snapshot.collection() ).items[0]["name"] )

asyncio.run( main() )
