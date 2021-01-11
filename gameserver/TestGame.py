import asyncio
from src.simulation.Simulator import Simulator
from src.player.FakePlayer import FakePlayer


async def testGame():
    """
    00000000000
    00000A00000
    00000000000
    00000M00000
    00000C00000
    00000000000
    00000000000
    00000000000
    00000000000
    00000000000
    00000000000
    """
    base = "0000000000000000A000000000000000000000M0000000000C00000000000000000000000000000000000000000000000000000000000000000000000"
    sim = Simulator(base, 0)
    player1 = FakePlayer()
    player2 = FakePlayer()
    await sim.startSimulating(player1, player2)


loop = asyncio.get_event_loop()
loop.run_until_complete(testGame())
loop.close()