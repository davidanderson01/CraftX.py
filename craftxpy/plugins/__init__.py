"""CraftX.py Plugins Module

This module contains the plugin system and base plugin functionality.
"""

from .base import BasePlugin, DemoPlugin, BaseModelPlugin
from .codegeex4 import CodeGeeX4
from .commandr7b import CommandR7B
from .qwen25coder import Qwen25Coder
from .wizardcoder import WizardCoder
from .craftx import CraftXModel

__all__ = [
    'BasePlugin',
    'BaseModelPlugin',
    'DemoPlugin',
    'CodeGeeX4',
    'CommandR7B',
    'Qwen25Coder',
    'WizardCoder',
    'CraftXModel',
]
