import asyncio
from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    async with rtbnext( client= ClientIdentity(
        name= "python-sdk-test",
        version= "1.0.0",
        contact="https://pypi.org/project/rtbnext"
    ) ) as client:

        # filter profiles
        female = await client.filter.gender( "f" ).collection()
        print( "Female profiles:", female.count )

        for item in female.take( 10 ):
            print( item.raw["name"], item.raw["uri"] )

        # use filter index ---

        index = await client.filter.index.get()
        us = await index["country"]["US"].collection()
        print( "U.S. profiles:", us.count )

        for item in us.take( 10 ):
            print( item.raw["name"], item.raw["uri"] )

        # complex filter queries
        tech = await client.filter.industry( "technology" ).collection()
        age_40_49 = await client.filter.age( "40" ).collection()
        profiles = female.intersect( tech ).intersect( age_40_49 )

        print( "Matching profiles:", profiles.count )

        for item in profiles:
            print( item.raw["name"], item.raw["uri"] )


asyncio.run( main() )
