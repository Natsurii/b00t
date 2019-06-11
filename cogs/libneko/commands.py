#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# MIT License
#
# Copyright (c) 2018 Neko404NotFound
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in a$
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Various addons and fixes/modifications to the Command, Group, and mixin
classes in Discord.py. There are also a bunch of new converter classes here,
and some checks and decorators.

Note:
    This is designed to be used in-place of :mod:`discord.ext.commands`.

Changes include:
    - Generators for qualified alias names
    - Generator for the name and aliases together.
    - Commands can be called directly to just invoke the logic without
      any prerequisites.
    - Groups now pass on their checks to their children implicitly.
    - Group behaviour defaults to invoke the group body only if no
      subcommand is matched first (``invoke_without_command`` defaults
      to be True).

New features include:
    - Checks for any channel type, categories, cogs, commands, snowflakes,
      generic mentions of arbitrary nature, etc.
    - An ``attr_generator`` that generates decorators for commands to
      associate various attributes with a command. If unspecified then
      they are assumed to be None.
    - A usage message generator using command signatures in a group or command.
    - ACK function that produces a reaction to the given
      message or context as an acknowledgement of some action. Defaults to
      the OK hand sign emoji, and removes itself after a few seconds.


Author:
    Espy/Neko404NotFound
"""
import asyncio
import traceback
from collections import defaultdict
import re
from typing import Iterator

from discord.ext import commands as _dpycommands
from discord.ext.commands.context import *
from discord.ext.commands.core import *

# noinspection PyUnresolvedReferences
from discord.ext.commands.cooldowns import *

# noinspection PyUnresolvedReferences
from discord.ext.commands.errors import *

from libneko import funcmods


# noinspection PyUnresolvedReferences
from libneko.attr_generator import attr_generator


# noinspection PyUnresolvedReferences
class CommandMixin:
    """
    Command implementation mixin that provides:
        - A builtin ``__command_attributes__`` to store basic attribute flags.
        - A ``category`` attribute that can be set in the constructor.
        - A ``examples`` attribute that can be set in the constructor.
        - ``all_names`` generator property that yields all names and aliases.
        - ``qualified_name`` property.
        - ``qualified_aliases`` property.
        - ``all_qualified_names`` property.

    Keyword Arguments:
        command_attributes:
            key-value attributes to associate with the object. See :meth:``attr_generator`` for a
            more in-depth discussion of this system.
        category: 
            optional category to give the command.
        examples:
            optional list of examples of usage to give the command.

    """

    def __init__(self, *args, **kwargs):
        self.__command_attributes__ = kwargs.pop("command_attributes", defaultdict(None))
        self.category = kwargs.pop("category", None)
        self.examples = kwargs.pop("examples", ())

    @property
    def attributes(self):
        return self.__command_attributes__

    @property
    def all_names(self) -> Iterator[str]:
        """
        The command name, and all aliases.
        """
        yield self.name
        yield from self.aliases

    @property
    def qualified_name(self) -> str:
        """
        Gets the command's qualified name (that is, appended to all parents
        to show ownership).
        """
        if self.parent:
            return f"{self.parent.qualified_name} {self.name}"
        else:
            return self.name

    @property
    def qualified_aliases(self) -> Iterator[str]:
        """
        Similar to ``qualified_name``, this outputs an iterator of qualified
        aliases.
        """
        fmt = "{0.qualified_name} {1}" if self.parent else "{1}"

        for alias in self.aliases:
            yield fmt.format(self.parent, alias)

    @property
    def all_qualified_names(self) -> Iterator[str]:
        """
        A concatenation of the qualified name, and qualified aliases, as an iterator.
        """
        yield self.qualified_name
        yield from self.qualified_aliases

    async def __call__(self, *args, **kwargs):
        """|coro|

        Invokes the command logic directly.
        """
        return await self.callback(*args, **kwargs)

    @classmethod
    @funcmods.steal_signature_from(_dpycommands.command)
    def create(cls, *args, **kwargs):
        """
        This is a functional decorator to initialise an instance of this class.

        Purpose being that you can assign a global attribute the value of this
        function. This way, you don't have to go through deriving your own
        decorators for each custom command implementation you provide.

        To make a decorator for a class ``Foo`` that derives from this mixin,
        just do::

            command = Foo.create

            ...

            @command()
            async def foo_command(ctx):
                ...

        """
        kwargs.setdefault("cls", cls)
        return _dpycommands.command(*args, **kwargs)

    def __repr__(self):
        return f"<Command {self.qualified_name} at {hex(id(self))}"


# noinspection PyUnresolvedReferences
class GroupMixin:
    """
    A group mixin type. Not to be confused with ``discord.ext.commands.GroupMixin``.
    """

    @funcmods.steal_signature_from(_dpycommands.Group.command)
    def command(self, *args, **kwargs):
        """
        Produces a decorator that decorates a coroutine to create a command
        object from it, adding it to this group.

        See the ``command`` decorator provided in this module.
        """
        kwargs.setdefault("cls", Command)
        return super().command(*args, **kwargs)

    @funcmods.steal_signature_from(_dpycommands.Group.group)
    def group(self, *args, **kwargs):
        """
        Produces a decorator that decorates a coroutine to create a command group
        object from it, adding it to this group.

        See the ``group`` decorator provided in this module.
        """
        kwargs.setdefault("cls", Group)
        return super().command(*args, **kwargs)

    def walk_youngest_descendants(self):
        """
        Iterates over the bottom-most nodes in the command tree that are
        descendants of this group.
        """
        for subcommand in frozenset(self.walk_commands()):
            if not isinstance(subcommand, GroupMixin):
                yield subcommand


class Command(_dpycommands.Command, CommandMixin):
    """
    Command implementation that implements ``discord.ext.commands.Command`` and ``CommandMixin``.

    Arguments from ``discord.ext.commands.Command``:
        callback:
            The coroutine that is executed when the command is called.

    Keyword Arguments from ``CommandMixin``:
        command_attributes: :class:`dict`
            key-value attributes to associate with the object.
        category: :class:`str`
            optional category to give the command.
        examples: :class:`list`
            optional list of examples of usage to give the command.

    Keyword Arguments from ``discord.ext.commands.Command``:
        name: :class:`str`
            The name of the command.
        help: :class:`str`
            The long help text for the command.
        brief: :class:`str`
            The short help text for the command. If this is not specified
            then the first line of the long help text is used instead.
        usage: :class:`str`
            A replacement for arguments in the default help text.
        aliases: :class:`list`
            The list of aliases the command can be invoked under.
        enabled: :class:`bool`
            A boolean that indicates if the command is currently enabled.
            If the command is invoked while it is disabled, then
            :exc:`.DisabledCommand` is raised to the :func:`.on_command_error`
            event. Defaults to ``True``.
        parent: Optional[command]
            The parent command that this command belongs to. ``None`` is there
            isn't one.
        checks:
            A list of predicates that verifies if the command could be executed
            with the given :class:`.Context` as the sole parameter. If an exception
            is necessary to be thrown to signal failure, then one derived from
            :exc:`.CommandError` should be used. Note that if the checks fail then
            :exc:`.CheckFailure` exception is raised to the :func:`.on_command_error`
            event.
        description: :class:`str`
            The message prefixed into the default help command.
        hidden: :class:`bool`
            If ``True``\, the default help command does not show this in the
            help output.
        rest_is_raw: :class:`bool`
            If ``False`` and a keyword-only argument is provided then the keyword
            only argument is stripped and handled as if it was a regular argument
            that handles :exc:`.MissingRequiredArgument` and default values in a
            regular matter rather than passing the rest completely raw. If ``True``
            then the keyword-only argument will pass in the rest of the arguments
            in a completely raw matter. Defaults to ``False``.
        ignore_extra: :class:`bool`
            If ``True``\, ignores extraneous strings passed to a command if all its
            requirements are met (e.g. ``?foo a b c`` when only expecting ``a``
            and ``b``). Otherwise :func:`.on_command_error` and local error handlers
            are called with :exc:`.TooManyArguments`. Defaults to ``True``.

    """

    def __init__(self, *args, **kwargs):
        _dpycommands.Command.__init__(self, *args, **kwargs)
        CommandMixin.__init__(self, *args, **kwargs)


class Group(GroupMixin, _dpycommands.Group, CommandMixin):
    """
    Group command implementation.

    Keyword Arguments from ``CommandMixin``:
        command_attributes: :class:`dict`
            key-value attributes to associate with the object.
        category: :class:`str`
            optional category to give the command.
        examples: :class:`list`
            optional list of examples of usage to give the command.

    Keyword Arguments from ``discord.ext.commands.Command``:
        name: :class:`str`
            The name of the command.
        help: :class:`str`
            The long help text for the command.
        brief: :class:`str`
            The short help text for the command. If this is not specified
            then the first line of the long help text is used instead.
        usage: :class:`str`
            A replacement for arguments in the default help text.
        aliases: :class:`list`
            The list of aliases the command can be invoked under.
        enabled: :class:`bool`
            A boolean that indicates if the command is currently enabled.
            If the command is invoked while it is disabled, then
            :exc:`.DisabledCommand` is raised to the :func:`.on_command_error`
            event. Defaults to ``True``.
        parent: Optional[command]
            The parent command that this command belongs to. ``None`` is there
            isn't one.
        checks
            A list of predicates that verifies if the command could be executed
            with the given :class:`.Context` as the sole parameter. If an exception
            is necessary to be thrown to signal failure, then one derived from
            :exc:`.CommandError` should be used. Note that if the checks fail then
            :exc:`.CheckFailure` exception is raised to the :func:`.on_command_error`
            event.
        description: :class:`str`
            The message prefixed into the default help command.
        hidden: :class:`bool`
            If ``True``\, the default help command does not show this in the
            help output.
        rest_is_raw: :class:`bool`
            If ``False`` and a keyword-only argument is provided then the keyword
            only argument is stripped and handled as if it was a regular argument
            that handles :exc:`.MissingRequiredArgument` and default values in a
            regular matter rather than passing the rest completely raw. If ``True``
            then the keyword-only argument will pass in the rest of the arguments
            in a completely raw matter. Defaults to ``False``.
        ignore_extra: :class:`bool`
            If ``True``\, ignores extraneous strings passed to a command if all its
            requirements are met (e.g. ``?foo a b c`` when only expecting ``a``
            and ``b``). Otherwise :func:`.on_command_error` and local error handlers
            are called with :exc:`.TooManyArguments`. Defaults to ``True``.

    Keyword Arguments from ``discord.ext.commands.Group``:
        all_commands: :class:`dict`
            A mapping of command name to :class:`.Command` or superclass
            objects.
        case_insensitive: :class:`bool`
            True if the group should pick out commands ignoring case.
        invoke_without_command: :class:`bool`
            If true, the group body is only called if no inner child command is
            matched. This is the default, unlike the discord.py implementation.

    """

    @funcmods.steal_signature_from(_dpycommands.Group.__init__)
    def __init__(self, *, invoke_without_command=True, **kwargs):
        """
        Init this group.

        This is the same as the discord.py version, but
        we invoke without command by default.
        """
        GroupMixin.__init__(self)
        _dpycommands.Group.__init__(self, invoke_without_command=invoke_without_command, **kwargs)
        CommandMixin.__init__(self, **kwargs)

    def add_command(self, command):
        """
        Adds a command to this group. Any checks on the group itself are
        inherited onto the child."
        """
        for check in self.checks:
            command.checks.append(check)
        return super().add_command(command)


#: Decorator for a command class. Works the same as the one in discord.ext.commands.
@funcmods.steal_signature_from(_dpycommands.command)
@funcmods.steal_docstring_from(_dpycommands.command)
def command(*args, **kwargs):
    kwargs.setdefault("cls", Command)

    def decorator(coro):
        return _dpycommands.command(*args, **kwargs)(coro)

    return decorator


#: Decorator for a group class. Works the same as the one in discord.ext.commands.
@funcmods.steal_signature_from(_dpycommands.group)
@funcmods.steal_docstring_from(_dpycommands.group)
def group(*args, **kwargs):
    kwargs.setdefault("cls", Group)

    def decorator(coro):
        return _dpycommands.command(*args, **kwargs)(coro)

    return decorator


async def get_user_from_mention(mention_str, users):
    """|coro|

    Picks out the user from the given string containing a mention.

    Applies to the first mention im the string only.

    If no user is found, we return None. If no mention is in the string,
    a value error is raised.

    Example usage::

        u = await get_user_from_mention('<@123456789> lol', ctx.guild.members)

    """
    try:
        id = int(re.findall(r"<@!?(\d+)>", mention_str)[0])
        return discord.utils.find(lambda m: m.id == id, users)
    except ValueError:
        raise ValueError("This is not a user mention.") from None


def reinvoke_on_edit(
    ctx: Context, *additional_messages: discord.Message, timeout: float = 600
) -> None:
    # noinspection PyUnresolvedReferences
    """
    Watches a given context for a given period of time. If the message that
    invoked the context is edited within the time period, then the invoking message
    plus any additional messages are deleted. The context's command is then reinvoked
    with the new message body.

    Parameters:
        ctx:
            A :class:`discord.ext.commands.Context` to listen to. Create one with
            `bot.get_context` if you are in an event instead.
        additional_messages:
            Any additional messages to also destroy on close.
        timeout:
            The timeout to wait for before the call terminates. This defaults to `None`, which is
            a special case depending on whether or not the `ctx` that was passed was actually a
            `BaseNavigator` object. If the latter holds, then the timeout will trigger as soon as
            the navigator timeout triggers.

    Note:
        To invoke this on a response that is being paginated using the `libneko.pag` module, you
        should attempt to invoke it like so::

        >>> factory = ...
        >>> nav = factory.build()
        >>> nav.start(ctx)
        >>> reinvoke_on_edit(ctx, *nav.all_messages)
        >>>
        >>> # or if you just have a nav
        >>>
        >>> nav = StringNavigator(...)
        >>> nav.start()
        >>> reinvoke_on_edit(ctx, *nav.all_messages)
    """

    if ctx.command is None:
        raise ValueError("Cannot reinvoke a non-valid command or non-command invocation")

    async def handle_wait_for_edit_or_close():
        try:
            # Triggered when we should kill our events.
            event = asyncio.Event()

            def set_on_exit(f):
                @funcmods.wraps(f)
                async def wrapper():
                    r = await f()
                    event.set()
                    return r

                return wrapper

            @set_on_exit
            async def wait_for_close():
                try:
                    await ctx.bot.wait_for(
                        "message_delete", check=lambda m: m.id == ctx.message.id, timeout=timeout
                    )
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    pass

            @set_on_exit
            async def wait_for_edit():
                try:

                    def predicate(before, after):
                        try:
                            # Only respond to this message
                            if after.id != ctx.message.id:
                                return False
                            elif before.content == after.content:
                                # Again, something went weird.
                                return False
                            elif not after.content.startswith(ctx.prefix):
                                return False
                            else:
                                # Ensure same command.
                                invoked = ctx.message.content[len(ctx.prefix) :].lstrip()
                                return invoked.startswith(ctx.invoked_with)
                        except Exception:
                            traceback.print_exc()

                    _, after = await ctx.bot.wait_for("message_edit", check=predicate)

                    new_ctx = await ctx.bot.get_context(after)

                    asyncio.ensure_future(
                        asyncio.gather(*[m.delete() for m in additional_messages]),
                        loop=ctx.bot.loop,
                    )

                    ctx.bot.loop.create_task(ctx.command.reinvoke(new_ctx))
                except asyncio.CancelledError:
                    pass
                except Exception:
                    traceback.print_exc()

            tasks = [
                ctx.bot.loop.create_task(wait_for_close()),
                ctx.bot.loop.create_task(wait_for_edit()),
            ]

            # On either of these events triggering, we kill the lot.
            await event.wait()

            for task in tasks:
                try:
                    task.cancel()
                    task.result()
                except Exception:
                    pass
        except Exception:
            traceback.print_exc()

    ctx.bot.loop.create_task(handle_wait_for_edit_or_close())


# noinspection PyUnresolvedReferences
async def get_usage(ctx):
    """|coro|

    Returns a list of usage examples for the given command in the given context.

    Example usage::

        @commands.group()
        async def some_group(ctx):
            return await ctx.send(get_usage(ctx))

        @some_group.command()
        async def some_command(ctx):
            ...
    """
    valid_subcommands = 0

    lines = []

    is_owner = ctx.author.id == ctx.bot.owner_id

    if isinstance(ctx.command, GroupMixin):
        for command in sorted(set(ctx.command.walk_commands()), key=str):
            try:
                suppressed = command.__command_attributes__.get(
                    "suppress_from_usage_message", False
                )
                can_run = is_owner or await command.can_run(ctx)

                if can_run and not suppressed:
                    lines.append(f"  {ctx.prefix}{command.signature}")
                    valid_subcommands += 1

            except Exception:
                pass

        if not valid_subcommands:
            lines.append("  Nothing is available for you.")
    else:
        try:
            can_run = await ctx.command.can_run(ctx)
        except Exception:
            can_run = False

        prefix = ctx.prefix

        lines.append(
            f"  {prefix}{ctx.command.signature}"
            if can_run
            else "  You lack permission to run this."
        )
    return lines


# noinspection PyUnresolvedReferences
async def send_usage(ctx):
    """|coro|

    Responds to a given message with some usage info. This is obtained by
    recursively traversing all parent commands.

    This will not check the length of the output. That
    is up to you to handle.

    Example usage::

        @commands.group()
        async def some_group(ctx):
            return await send_usage(ctx)

        @some_group.command()
        async def some_command(ctx):
            ...

    """
    lines = await get_usage(ctx)
    nl = "\n"
    await ctx.send(f"```\nUSAGE:\n{nl.join(lines)}\n```")


def suppress_from_usage_message():
    """
    Decorates a command that can have the `get_usage` or `send_usage` coroutines
    inspect it, and requests that the message skip their definitions.

    Example usage::

        @suppress_from_usage_message()
        @commands.command(...)
        async def ...(...):
            ...

    """
    return attr_generator("suppress_from_usage_message", True)
