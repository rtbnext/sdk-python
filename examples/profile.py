import asyncio
from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    async with rtbnext( client= ClientIdentity(
        name= "python-sdk-test",
        version= "1.0.0",
        contact="https://pypi.org/project/rtbnext"
    ) ) as client:

        # access profile data
        data = await client.profile.data( "bill-gates" ).data()
        print( data["bio"]["cv"], ( data.get( "wiki" ) or {} ).get( "desc" ) )

        # use the profile index collection
        index = await client.profile.index.collection()
        print( "Total:", index.total )

        for item in index.search( "space" ).order_by( "networth", descending= True ).take( 5 ):
            print( item.raw["name"], item.raw["uri"] )

        # work with profile history
        history = await client.profile.get( "elon-musk" ).history.series()
        print( "Points:", history.count )
        print( "Latest:", history.first )
        print( "Average:", history.avg( lambda p: p["networth"] ) )


asyncio.run( main() )
