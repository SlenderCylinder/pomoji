from . import config


SUMMARY = 'Hi Joanna,\n' \
          'Required parameters are enclosed in <> and optional parameters are enclosed in [].\n' \
          f'For example, you can do \"{config.CMD_PREFIX}start\" to start a pomodoro session with the default values ' \
          f'or \"{config.CMD_PREFIX}start 30 10\" to customize the pomodoro and short break durations!\n'

POMO_ARGS = 'pomodoro: duration of each pomodoro interval in minutes (Default: 20 min)\n' \
            'short_break: duration of short breaks in minutes (Default: 5 min)\n' \
            'long_break: duration of long breaks in minutes (Default: 15 min)\n' \
            'intervals: number of pomodoro intervals between each long break (Default: 4)'

COUNTDOWN_ARGS = 'Enclose title in " " if longer than one word (Default: \"Countdown\").\n' \
                 'Add the \"mute\" parameter to disable the voice channel audio alert.\n\n' \
                 f'Example usage: {config.CMD_PREFIX}countdown 5 \"Finish homework!\" mute'

COMMANDS = {'Control commands': {'start': ['start [pomodoro] [short_break] [long_break] [intervals]',
                                           'Start pomodoro session with optional custom settings.\n\n' + POMO_ARGS],
                                 'pause': ['pause', 'Pause session'],
                                 'resume': ['resume', 'Resume session'],
                                 'restart': ['restart', 'Restart timer'],
                                 'skip': ['skip', 'Skip current interval and start the next pomodoro or break.'],
                                 'stop': ['stop', 'End session'],
                                 'edit': ['edit <pomodoro> [short_break] [long_break] [intervals]',
                                          'Continue session with new settings\n\n' + POMO_ARGS],
                                 'countdown': ['countdown <duration> [title] [mute]',
                                               'Start a countdown which sends a pinned message '
                                               'with a timer that updates in real time.\n\n' +
                                               COUNTDOWN_ARGS]
                                 },
            'Info commands': {'time': ['time', 'Get time remaining'],
                              'stats': ['stats', 'Get session stats'],
                              'settings': ['settings', 'Get session settings'],
                              'servers': ['servers', 'See how many servers are using Pomomo']},
            'Subscription commands': {'dm': ['dm', 'Toggle subscription to get DM alerts for the server\'s session.'],
                                      'autoshush': ['autoshush [all]', 'Toggle subscription to get automatically'
                                                                       ' deafened and muted during '
                                                                       'pomodoro intervals.\n'
                                                                       'Members with mute and deafen permissions '
                                                                       'can add the \"all\" parameter to auto_shush '
                                                                       'everyone in the pomodoro voice channel.']}}

LINKS = ''
