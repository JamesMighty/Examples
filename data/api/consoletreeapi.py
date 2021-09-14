import subprocess
import sys

from data.resources.command import Command
from data.lib.datastore.context import Context


class RunCmdCommand(Command):

    def __call__(self, context: Context, query: str, input: str) -> str:
        match = input[0][0]
        args = match.split(" ")
        process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
        out, err = process.communicate()
        if out:
            return bytes.decode(out) 
        else:
            return ""

class PopenCommand(Command):

    def __call__(self, context: Context, query: str, input: str) -> str:
        match = input[0][0]
        args = match.split(" ")
        process = subprocess.Popen(args, stdout=subprocess.PIPE)
        out, err = process.communicate()
        if out:
            return bytes.decode(out) 
        else:
            return ""
    

