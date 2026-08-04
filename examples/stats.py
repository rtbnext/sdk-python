import asyncio
from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    async with rtbnext( client= ClientIdentity(
        name= "python-sdk-test",
        version= "1",
        contact="https://pypi.org/project/rtbnext"
    ) ) as client:

        # get global stats
        stats = await client.stats.global_.data()
        print( "Global stats:" )
        print( "Profiles:", stats["count"] )
        print( "Total wealth:", stats["total"] )
        print( "Woman quota:", stats["quota"] )

        # work with profile scatter data
        scatter = await client.stats.scatter.collection()
        print( "Scatter points:", scatter.count )

        for point in scatter.take( 10 ):
            print( point.raw["name"], point.raw["networth"], point.raw["age"] )

        # access history time series
        history = await client.stats.history.series()
        print( "History points:", history.count )
        print( "Newest:", history.latest )
        print( "Average profiles:", history.avg( lambda p : p["count"] ) )

        for year in history.aggregate( "year" ):
            print( year["label"], year["count"]["last"], year["total"]["avg"] )

        # navigate through time series points

        page = history.page( 1 )
        while ( item := page.next ) is not None:
            print( item["date"], item["count"], item["total"] )


asyncio.run( main() )
