import random
import time as t
from discord import Embed, Colour
from discord.ext import commands
from .Session import Session
from . import session_manager, session_controller
from ..utils import msg_builder
from configs import user_messages as u_msg
from asyncio import sleep
from configs import bot_enum
import requests
import json

quote=msg_builder.get_quote()

async def send_start_msg(session: Session):
      await session.ctx.send(random.choice(u_msg.GREETINGS),embed=msg_builder.settings_embed(session))
      quote=msg_builder.get_quote()
      embed= Embed(title="Random quote", description=quote, color=0x18d5d0)
      await session.ctx.send(embed=embed)
      settings = session.settings
      start_str = f'**{settings.duration} min** pomodor session; _starting now_...'
      await session.ctx.send(start_str)

      
"""async def send_start_timer(session: Session):
    embed = Embed(description=f'{session.timer.time_remaining_to_str()} remaining on {session.state}!', colour=Colour.green())
    session.bot_timer_msg = await session.ctx.send(embed=embed)
    await session.bot_timer_msg.pin()
    session = session_manager.active_sessions.get(session_manager.session_id_from(session.ctx.channel))
    while True:
      embed = Embed(description=f'{session.timer.time_remaining_to_str()} remaining on {session.state}!', colour=Colour.green())
      await session.bot_timer_msg.edit(embed=embed)

async def send_edit_msg(session: Session):
      await session.ctx.send('Continuing pomodoro session with new settings!',
                           embed=msg_builder.settings_embed(session))"""


async def send_countdown_msg(session: Session, title: str):
    title += '\u2800' * max((18 - len(title)), 0)
    embed = Embed(title=title, description=f'{session.timer.time_remaining_to_str()} left!', colour=Colour.green())
    session.bot_start_msg = await session.ctx.send(embed=embed)
    await session.bot_start_msg.pin()
