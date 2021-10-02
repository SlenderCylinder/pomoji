import time as t

from discord.ext import commands
from discord import Embed, Colour
from src.Settings import Settings
from configs import config, bot_enum, user_messages as u_msg
from src.session import session_manager, session_controller, session_messenger, countdown, state_handler
from discord.ext.commands import CommandNotFound
from src.session.Session import Session
from src.utils import msg_builder
import ffmpeg
import random

class Control(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def start(self, ctx, pomodoro=20, short_break=5, long_break=15, intervals=4):
        if not await Settings.is_valid(ctx, pomodoro, short_break, long_break, intervals):
            return
        if session_manager.active_sessions.get(session_manager.session_id_from(ctx.channel)):
            await ctx.send(u_msg.ACTIVE_SESSION_EXISTS_ERR)
            return
        if not ctx.author.voice:
            await ctx.send('Join a voice channel to use Pomoji!')
            return
        session = Session(bot_enum.State.POMODORO,
                          Settings(pomodoro, short_break, long_break, intervals),
                          ctx)
        await session_controller.start(session)
    @start.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR)
        else:
            print(error)

    @commands.command()
    async def stop(self, ctx):
        embed = Embed(colour=Colour.red())
        image = random.choice(["https://c.tenor.com/bouurkbU61gAAAAC/milkmocha-milk-and-mocha.gif",
        "https://c.tenor.com/lGCSPV9_eGsAAAAC/milk-and-mocha-bears-ok.gif", 
        "https://c.tenor.com/aFDActHjaokAAAAC/milk-and-mocha-food.gif",
        "https://c.tenor.com/YgsIQLSFeEoAAAAC/milk-and-mocha-bears-yeah.gif",
        "https://c.tenor.com/vkby5v7ABWMAAAAC/milk-and-mocha-bears-disco.gif",
        "https://c.tenor.com/JI-wBFXNZw8AAAAC/milk-and-mocha-cute.gif"]
        )
        embed.set_image(url=image)
        session = await session_manager.get_session(ctx)
        session.timer2.running1 = False
        session.timer.running = False
        if session:
            user = ctx.author
            if session.stats.pomos_completed > 0:
                if ctx.author.id == 694679380068270170:
                                    await ctx.send(f'Great job, Joanna! '
                               f'You completed {msg_builder.stats_msg(session.stats)}')
                                    await ctx.send(embed=embed)
                if ctx.author.id == 490687063692279818:
                                    await ctx.send(f'Great job, Chamith! '
                               f'You completed {msg_builder.stats_msg(session.stats)}')
                                    await ctx.send(embed=embed)               
            else:                   
                if ctx.author.id == 694679380068270170:
                    await ctx.send(f'See you again soon, Joanna! 👋') 
                if ctx.author.id == 490687063692279818:
                    await ctx.send(f'See you again soon, Chamith! 👋')
            await session_controller.end(session)


    @commands.command()
    async def pause(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            timer = session.timer
            if not timer.running:
                await ctx.send('Timer is already paused.')
                return

            await session.auto_shush.unshush(ctx)
            timer.running = False
            timer.remaining = timer.end - t.time()
            await ctx.send(f'Pausing {session.state}.')
            session.timeout = t.time() + config.PAUSE_TIMEOUT_SECONDS

    @commands.command()
    async def resume(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            timer = session.timer
            if session.timer.running:
                await ctx.send('Timer is already running.')
                return

            timer.running = True
            timer.end = t.time() + timer.remaining
            await ctx.send(f'Resuming {session.state}.')
            await session_controller.resume(session)

    @commands.command()
    async def restart(self, ctx):
        session = await session_manager.get_session(ctx)
        if session:
            session.timer.set_time_remaining()
            await ctx.send(f'Restarting {session.state}.')
            if session.state == bot_enum.State.COUNTDOWN:
                await countdown.start(session)
            else:
                await session_controller.resume(session)

    @commands.command()
    async def skip(self, ctx):
        session = await session_manager.get_session(ctx)
        if session.state == bot_enum.State.COUNTDOWN:
            ctx.send(f'Countdowns cannot be skipped. '
                     f'Use {config.CMD_PREFIX}stop to end or {config.CMD_PREFIX}restart to start over.')
        if session:
            stats = session.stats
            if stats.pomos_completed >= 0 and \
                    session.state == bot_enum.State.POMODORO:
                stats.pomos_completed -= 1
                stats.minutes_completed -= session.settings.duration

            await ctx.send(f'Skipping {session.state}.')
            await state_handler.transition(session)
            await session_controller.resume(session)

    @commands.command()
    async def edit(self, ctx, pomodoro: int, short_break: int = None, long_break: int = None, intervals: int = None):
        session = await session_manager.get_session(ctx)
        if session.state == bot_enum.State.COUNTDOWN:
            ctx.send(f'Countdowns cannot be edited. '
                     f'Use {config.CMD_PREFIX}countdown to start a new one.')
        if session:
            if not await Settings.is_valid(ctx, pomodoro, short_break, long_break, intervals):
                return
            await session_controller.edit(session, Settings(pomodoro, short_break, long_break, intervals))
            session.timer.set_time_remaining()
            if session.state == bot_enum.State.COUNTDOWN:
                await countdown.update_msg(session)
            await session_controller.resume(session)

    @edit.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(u_msg.MISSING_ARG_ERR)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR)
        else:
            print(error)

    @commands.command()
    async def countdown(self, ctx, duration: int, title='Countdown', audio_alert=None):
        session = session_manager.active_sessions.get(session_manager.session_id_from(ctx.channel))
        if session:
            await ctx.send('There is an active session running. '
                           'Are you sure you want to start a countdown? (y/n)')
            response = await self.client.wait_for('message', timeout=60)
            if not response.content.lower()[0] == 'y':
                await ctx.send('OK, cancelling new countdown.')
                return

        if not 0 < duration <= 180:
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR)
        session = Session(bot_enum.State.COUNTDOWN,
                          Settings(duration),
                          ctx)
        await countdown.handle_connection(session, audio_alert)
        session_manager.activate(session)
        await session_messenger.send_countdown_msg(session, title)
        await countdown.start(session)

    @countdown.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(u_msg.MISSING_ARG_ERR)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(u_msg.NUM_OUTSIDE_ONE_AND_MAX_INTERVAL_ERR)
        else:
            print(error)
def setup(client):
    client.add_cog(Control(client))

async def handle_error(self,ctx,error):
        if isinstance(error, commands.CommandNotFound):
           await ctx.send("Command does not exist.")