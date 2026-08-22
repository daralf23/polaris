from dataclasses import dataclass


@dataclass
class PluginContext:
    logger: any
    config: any
    http: any = None
    dispatcher: any = None
    scheduler: any = None
    state: any = None
