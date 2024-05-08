import importlib
import time
import re
from pathlib import Path
from collections.abc import Callable, Coroutine, Iterable, Sequence
from .logger import logger


class PluginError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Result:
    def __init__(self, send_method: str, data) -> None:
        self.send_method = send_method
        self.data = data


class Event:
    def __init__(
        self,
        raw_command: str,
        args: Sequence[str],
    ):
        self.raw_command = raw_command
        self.args = args
        self.kwargs: dict = {}
        self.get_kwargs: dict[str, Callable[..., Coroutine]] = {}


class Handle:
    func: Callable[[Event], Coroutine[None, None, Result | None]]

    def __init__(self, extra_args: Iterable[str], get_extra_args: Iterable[str]):
        self.extra_args = extra_args
        self.get_extra_args = get_extra_args

    async def __call__(self, event: Event):
        return await self.func(event)


PluginCommands = str | Iterable[str] | re.Pattern | None


class Plugin:
    def __init__(
        self,
        name: str = "",
        build_event=None,
        build_result=None,
    ) -> None:
        self.name: str = name
        self.handles: dict[int, Handle] = {}
        self.command_dict: dict[str, set[int]] = {}
        self.regex_dict: dict[re.Pattern, set[int]] = {}
        self.temp_handles: dict[str, tuple[float, Handle]] = {}
        self.startup_tasklist: list[Coroutine] = []
        self.shutdown_tasklist: list[Coroutine] = []
        self.build_event: Callable | None = build_event
        self.build_result: Callable | None = build_result

    def handle_warpper(self, func: Callable[..., Coroutine]):
        if build_event := self.build_event:
            middle_func = lambda e: func(build_event(e))
        else:
            middle_func = func

        if build_result := self.build_result:

            async def wrapper(event):
                if result := await middle_func(event):
                    return build_result(result)

            return wrapper
        else:
            return middle_func

    def commands_register(self, commands: PluginCommands, key: int):
        if not commands:
            self.command_dict.setdefault("", set()).add(key)
        elif isinstance(commands, str):
            self.regex_dict.setdefault(re.compile(commands), set()).add(key)
        elif isinstance(commands, re.Pattern):
            self.regex_dict.setdefault(commands, set()).add(key)
        elif isinstance(commands, Iterable):
            for command in commands:
                self.command_dict.setdefault(command, set()).add(key)
        else:
            raise PluginError(f"指令：{commands} 类型错误：{type(commands)}")

    def handle(
        self,
        commands: PluginCommands,
        extra_args: Iterable[str] = [],
        get_extra_args: Iterable[str] = [],
    ):
        def decorator(func: Callable[..., Coroutine]):
            key = len(self.handles)
            self.commands_register(commands, key)
            handle = Handle(extra_args, get_extra_args)
            handle.func = self.handle_warpper(func)
            self.handles[key] = handle

        return decorator

    class Finish:
        def __init__(
            self,
            temp_handles: dict[str, tuple[float, Handle]],
            key: str,
        ) -> None:
            self.handles = temp_handles
            self.key = key

        def __call__(self):
            del self.handles[self.key]

        def delay(self, timeout: float | int = 30.0):
            self.handles[self.key] = (time.time() + timeout, self.handles[self.key][1])

    def temp_handle(
        self,
        key: str,
        extra_args: Iterable[str] = [],
        get_extra_args: Iterable[str] = [],
        timeout: float | int = 30.0,
    ):

        def decorator(func: Callable[..., Coroutine]):
            handle = Handle(extra_args, get_extra_args)
            handle.func = self.handle_warpper(lambda e: func(e, self.Finish(self.temp_handles, key)))
            self.temp_handles[key] = time.time() + timeout, handle

        return decorator

    def startup(self, func: Callable[[], Coroutine]):
        """注册一个启动任务"""
        self.startup_tasklist.append(func())

        return func

    def shutdown(self, func: Callable[[], Coroutine]):
        """注册一个结束任务"""
        self.shutdown_tasklist.append(func())

        return func

    def __call__(self, command: str) -> dict[int, Event] | None:
        command_list = command.split()
        if not command_list:
            return
        data = {}
        command_start = command_list[0]
        for cmd, keys in self.command_dict.items():
            if not command_start.startswith(cmd):
                continue
            if command_start == cmd:
                args = command_list[1:]
            else:
                command_list[0] = command_list[0][len(cmd) :]
                args = command_list
            event = Event(command, args)
            data.update({key: event for key in keys})

        for pattern, keys in self.regex_dict.items():
            if args := re.match(pattern, command):
                event = Event(command, args.groups())
                data.update({key: event for key in keys})

        return data

    def temp_check(self) -> bool:
        if not self.temp_handles:
            return False
        now = time.time()
        self.temp_handles = {k: v for k, v in self.temp_handles.items() if v[0] > now}
        if not self.temp_handles:
            return False
        return True


class PluginLoader:
    def __init__(self, plugins_path: str | Path | None = None, plugins_list: list[str] = []) -> None:
        self.plugins_path: Path | None = None if plugins_path is None else Path(plugins_path)
        self.plugins_list: list = plugins_list

    @staticmethod
    def load(name: str) -> Plugin | None:
        logger.info(f"【loading plugin】 {name} ...")
        try:
            module = importlib.import_module(name)
            plugin = getattr(module, "__plugin__", None)
            if not isinstance(plugin, Plugin):
                return
            plugin.name = plugin.name or name
            return plugin
        except:
            logger.exception(name)

    def plugins_from_path(self) -> list[Plugin]:
        if self.plugins_path is None:
            return []
        plugins_path = ".".join(self.plugins_path.relative_to(Path()).parts)
        plugins = []
        for x in self.plugins_path.iterdir():
            name = x.stem if x.is_file() and x.name.endswith(".py") else x.name
            if name.startswith("_"):
                continue
            plugins.append(self.load(f"{plugins_path}.{name}"))
        return [plugin for plugin in plugins if plugin]

    def plugins_from_list(self) -> list[Plugin]:
        return [plugin for x in self.plugins_list if (plugin := self.load(x))]

    @property
    def plugins(self) -> list[Plugin]:
        return self.plugins_from_path() + self.plugins_from_list()
