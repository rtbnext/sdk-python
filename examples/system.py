import asyncio
from rtbnext import ClientIdentity, rtbnext


async def main() -> None:
    async with rtbnext( client= ClientIdentity(
        name= "python-sdk-test",
        version= "1.0.0"
    ) ) as client:

        # get current system status
        status = await client.system.status.data()
        print( "System status:", status["status"] )
        print( "Profile status:", status["services"]["profile"] )


asyncio.run( main() )
