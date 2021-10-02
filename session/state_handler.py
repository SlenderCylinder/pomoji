from .Session import Session
from configs import bot_enum
import random
from discord import Embed, Colour


async def transition(session: Session):
    embed = Embed(colour=Colour.green())
    image = random.choice(["https://c.tenor.com/6YaJ49psXl0AAAAC/gudetama-sad.gif",
      "https://c.tenor.com/ROGyVpmI9w4AAAAC/gudetama-scholar.gif",
      "https://c.tenor.com/jLlcmN87QHUAAAAC/gudetama-poop.gif",
      "https://c.tenor.com/opQ-c7hRqJYAAAAC/gut.gif",
      "https://c.tenor.com/2tp1_j-Uo-8AAAAi/gudetama-love.gif",])
    embed.set_image(url=image)
    session.timer.running = False
    if session.state == bot_enum.State.POMODORO:
        stats = session.stats
        stats.pomos_completed += 1
        stats.minutes_completed += session.settings.duration
        if stats.pomos_completed > 0 and\
                stats.pomos_completed % session.settings.intervals == 0:
            session.state = bot_enum.State.LONG_BREAK
        else:
            session.state = bot_enum.State.SHORT_BREAK
    else:
        session.state = bot_enum.State.POMODORO
        await session.auto_shush.shush(session.ctx)
    session.timer.set_time_remaining()
    alert = f'Starting {session.timer.time_remaining_to_str(singular=True)} {session.state}.'
    await session.ctx.send(alert)
    await session.dm.send_dm(alert)


async def auto_shush(session: Session):
    if session.state in [bot_enum.State.COUNTDOWN, bot_enum.State.POMODORO]:
        await session.auto_shush.shush(session.ctx)
    else:
        await session.auto_shush.unshush(session.ctx)
