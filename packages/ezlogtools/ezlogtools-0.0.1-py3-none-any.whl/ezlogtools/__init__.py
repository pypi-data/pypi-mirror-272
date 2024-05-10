from typing import TextIO

from enum import IntEnum, auto
import sys

import colorama

class Console:
    class Level(IntEnum):
        """
        critical > important > high > low
        """
        critical = auto()
        important = auto()
        high = auto()
        low = auto()

    current_logging_level = Level.low

    default_ostream = {
        'error': sys.stderr if sys.platform != 'win32' else colorama.AnsiToWin32(sys.stderr),
        'warn' : sys.stdout if sys.platform != 'win32' else colorama.AnsiToWin32(sys.stdout),
        'info' : sys.stdout if sys.platform != 'win32' else colorama.AnsiToWin32(sys.stdout),
        'log'  : sys.stdout if sys.platform != 'win32' else colorama.AnsiToWin32(sys.stdout),
    }
    default_level = {
        'error': Level.critical,
        'warn' : Level.important,
        'info' : Level.high,
        'log'  : Level.low,
    }

    @staticmethod
    def set_default_ostream(
        error: TextIO = None,
        warn : TextIO = None,
        info : TextIO = None,
        log  : TextIO = None,
        wrap_with_win32_color_bindings = sys.platform == 'win32'
    ):
        """
        Provide the default out streams for different logging functions
        When wrap_with_win32_color_bindings is set to True, wraps the TextIO with colorama's AnsiToWin32 wrapper
        NOTE: Will only wrap if the TextIO is sys.stderr or sys.stdout
        """
        if error is not None: Console.default_ostream['error'] = error if (not wrap_with_win32_color_bindings) or (error is not sys.stdout and error is not sys.stderr) else colorama.AnsiToWin32(error)
        if warn  is not None: Console.default_ostream['warn']  = warn  if (not wrap_with_win32_color_bindings) or (warn  is not sys.stdout and warn  is not sys.stderr) else colorama.AnsiToWin32(warn)
        if info  is not None: Console.default_ostream['info']  = info  if (not wrap_with_win32_color_bindings) or (info  is not sys.stdout and info  is not sys.stderr) else colorama.AnsiToWin32(info)
        if log   is not None: Console.default_ostream['log']   = log   if (not wrap_with_win32_color_bindings) or (log   is not sys.stdout and log   is not sys.stderr) else colorama.AnsiToWin32(log)

    @staticmethod
    def set_default_level(
        error: Level = None,
        warn : Level = None,
        info : Level = None,
        log  : Level = None,
    ):
        """
        Provide the default levels for different logging functions
        """
        if error is not None: Console.default_level['error'] = error
        if warn  is not None: Console.default_level['warn']  = warn
        if info  is not None: Console.default_level['info']  = info
        if log   is not None: Console.default_level['log']   = log

    @staticmethod
    def set_log_level(level: Level):
        """
        Set the log level that the console should use
        """
        old_logging_level = Console.current_logging_level
        Console.current_logging_level = level
        return old_logging_level

    @staticmethod
    def error(log, *additional, level: Level = None, ostream: TextIO = None):
        if level is None: level = Console.default_level['error']
        if level > Console.current_logging_level: return
        if ostream is None: ostream = Console.default_ostream['error']
        
        print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLACK_EX}[{colorama.Back.LIGHTRED_EX}{colorama.Fore.BLACK}    ERROR    {colorama.Fore.LIGHTBLACK_EX}{colorama.Back.RESET}]{colorama.Style.RESET_ALL} {colorama.Fore.LIGHTRED_EX}{log}", *additional, colorama.Fore.RESET, sep='\n', file=ostream)

    @staticmethod
    def warn(log, *additional, level: Level = None, ostream: TextIO = None):
        if level is None: level = Console.default_level['warn']
        if level > Console.current_logging_level: return
        if ostream is None: ostream = Console.default_ostream['warn']
        
        print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLACK_EX}[{colorama.Back.LIGHTMAGENTA_EX}{colorama.Fore.BLACK}   WARNING   {colorama.Fore.LIGHTBLACK_EX}{colorama.Back.RESET}]{colorama.Style.RESET_ALL} {colorama.Fore.LIGHTMAGENTA_EX}{log}", *additional, colorama.Fore.RESET, sep='\n', file=ostream)

    @staticmethod
    def info(log, *additional, level: Level = None, ostream: TextIO = None):
        if level is None: level = Console.default_level['info']
        if level > Console.current_logging_level: return
        if ostream is None: ostream = Console.default_ostream['info']

        print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLACK_EX}[{colorama.Back.LIGHTBLUE_EX}{colorama.Fore.BLACK} INFORMATION {colorama.Back.RESET}{colorama.Fore.LIGHTBLACK_EX}]{colorama.Style.RESET_ALL} {colorama.Fore.LIGHTCYAN_EX}{log}", *additional, colorama.Fore.RESET, sep='\n', file=ostream)
        
    @staticmethod
    def log(log, *additional, level: Level = None, ostream: TextIO = None):
        if level is None: level = Console.default_level['log']
        if level > Console.current_logging_level: return
        if ostream is None: ostream = Console.default_ostream['log']

        print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTBLACK_EX}[{colorama.Back.WHITE}{colorama.Fore.BLACK}     LOG     {colorama.Back.RESET}{colorama.Fore.LIGHTBLACK_EX}]{colorama.Style.RESET_ALL} {colorama.Fore.LIGHTWHITE_EX}{log}", *additional, colorama.Fore.RESET, sep='\n', file=ostream)
        