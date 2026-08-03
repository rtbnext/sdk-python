import asyncio
from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    async with rtbnext( client= ClientIdentity(
        name= "python-sdk-test",
        version= "1.0.0"
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
            print( point["name"], point["networth"], point["age"] )

        # access history time series
        history = await client.stats.history.series()
        print( "History points:", history.count )
        print( "Newest:", history.first )
        print( "Average profiles:", history.avg( lambda p : p["count"] ) )

        for year in history.aggregate( "year" ):
            print( year["label"], year["count"]["last"], year["total"]["avg"] )


asyncio.run( main() )
