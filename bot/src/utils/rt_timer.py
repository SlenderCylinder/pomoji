import random
import time as t
from discord import Embed, Colour
from discord.ext import commands
from src.session import Session
from src.session import session_manager, session_controller, session_messenger
from src.utils import msg_builder
from configs import user_messages as u_msg
from asyncio import sleep
from configs import bot_enum


async def send_start_timer(session: Session):
    embed = Embed(description=f'{session.timer.time_remaining_to_str()} remaining on {session.state}!', colour=Colour.green())
    session.bot_timer_msg = await session.ctx.send(embed=embed)
    await session.bot_timer_msg.pin()
    while session:
              embed = Embed(description=f'{session.timer.time_remaining_to_str()} remaining on {session.state}!', colour=Colour.green())
              await session.bot_timer_msg.edit(embed=embed)
