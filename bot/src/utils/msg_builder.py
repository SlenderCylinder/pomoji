from discord import Embed, Colour
import random
from configs import config, help_info
from ..Stats import Stats
from ..session.Session import Session
import requests
import json
import aiohttp

def settings_embed(session: Session) -> Embed:
    settings = session.settings
    settings_str = f'Pomodoro: {settings.duration} min\n' \
               f'Short break: {settings.short_break} min\n' \
               f'Long break: {settings.long_break} min\n' \
               f'Intervals: {settings.intervals}\n' 
    image = random.choice(["https://c.tenor.com/qrNqD3lvOq0AAAAC/milk-and-mocha-coffee.gif",
      "https://c.tenor.com/AywMdBYeX5oAAAAC/milk-and-mocha-yay.gif",
      "https://c.tenor.com/D4UWrImI444AAAAC/milk-and-mocha-dance.gif",
      "https://c.tenor.com/aBThlN6qrT0AAAAi/milk-and.gif",
      "https://c.tenor.com/m9XZQPmB-BgAAAAi/rascal-lets-do-this.gif",
      "https://c.tenor.com/aKFaZBrZFYcAAAAC/excited-spin.gif",
      "https://c.tenor.com/zU1hQV8SyiQAAAAd/you-got-this.gif",
      "https://c.tenor.com/cn0dFVS3OqAAAAAC/gudetama-tired.gif"])
    embed = Embed(title='Session settings', description=settings_str, colour=Colour.orange())
    embed.set_image(url=image)
    vc = session.ctx.voice_client
    if vc:
        footer = f'Connected to {vc.channel.name} voice channel'
        if session.auto_shush.all:
            footer += '\nAuto-shush is on'
        embed.set_footer(text=footer)
    return embed


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q']+" -"+ json_data[0]['a']
  return (quote) 

def help_embed(for_command) -> Embed:
    if for_command == '':
        embed = Embed(title='Help menu', description=help_info.SUMMARY, colour=Colour.blue())
        for cmds_key, cmds_dict in help_info.COMMANDS.items():
            values = ''
            for value in cmds_dict.values():
                values += f'{value[0]}\n'
            embed.add_field(name=cmds_key, value=values, inline=False)
        more_info = f'\nFor more info on a specific command, type \'{config.CMD_PREFIX}help [command]\'\n\n' \
                    + help_info.LINKS
        embed.add_field(name='\u200b', value=more_info, inline=False)
        return embed
    else:
        for cmds_key, cmds_dict in help_info.COMMANDS.items():
            cmd_info = cmds_dict.get(for_command)
            if cmd_info:
                return Embed(title=cmd_info[0], description=cmd_info[1], colour=Colour.blue())


def stats_msg(stats: Stats):
    pomo_str = 'pomodoros'
    minutes_str = 'minutes'
    hours_str: str
    if stats.minutes_completed >= 60:
        hours_str = 'hours'
        hours_completed = int(stats.minutes_completed/60)
        if hours_completed == 1:
            hours_str = 'hour'
        time_completed_str = f'{hours_completed} {hours_str}'
        minutes_completed = int(stats.minutes_completed % 60)
        if minutes_completed == 1:
            minutes_str = 'minute'
        if minutes_completed > 0:
            time_completed_str += f' {minutes_completed} {minutes_str}'
    else:
        if stats.minutes_completed == 1:
            minutes_str = 'minute'
        time_completed_str = f'{stats.minutes_completed} {minutes_str}'
    if stats.pomos_completed == 1:
        pomo_str = 'pomodoro'
    return f'{stats.pomos_completed} {pomo_str} ({time_completed_str})'
