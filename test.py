import asyncio

from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    client = rtbnext(
        client= ClientIdentity(
            name= "python-sdk-test",
            version= "1.0.0b1"
        )
    )

    index = await client.filter.index.get()
    woman = await index["gender"]["f"].collection()
    germany = await index["country"]["DE"].collection()
    print( woman.total, germany.total )


asyncio.run( main() )
