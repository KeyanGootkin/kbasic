# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from kbasic.bar import redirect_to_tqdm
from kbasic.audio import success
from kbasic.environment import isAnvil 
if isAnvil: from kbasic.environment.anvil import anvil_user
from typing import Any
from subprocess import check_output, DEVNULL
from tqdm import tqdm
from time import sleep
import asyncio

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                              Types                              <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
bad: list[str] = ['\x1b[31m', '\x1b[34m', '\x1b[m']
_USERNAME_: str = "x-kgootkin" if not isAnvil else anvil_user
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def parse_shell_output(output: str | list[str]) -> str | list[str]:
    """take the output of a shell command and make it nice

    Args:
        output (str | list[str]): the output of a shell command

    Returns:
        str | list[str]: a cleaned version of output
    """
    match output:
        case str(): return output 
        case [x]: return x
        case [x, *_]: 
            for i in range(len(output)):
                for b in bad:
                    if b in output[i]:
                        output[i] = output[i].strip(b)
            return output
def system(cmd: str) -> str | list[str]:
    """a version of os.system that actually can return the output

    Args:
        cmd (str): the command to give the terminal

    Returns:
        str | list[str]: the output of the command (cleaned of color tags)
    """
    command = cmd.split(' ') if type(cmd)==str else cmd
    for i in range(len(command)-1):
        if command[i].startswith('"'): 
            start_quote = i 
            end_quote = i+1
            while not command[end_quote].endswith('"'): end_quote+=1
            command[i] = " ".join(command[start_quote:end_quote+1])
            for j in range(start_quote+1, end_quote+1): del command[j]
    output = parse_shell_output(check_output(command, stderr=DEVNULL).decode().splitlines())
    return output
def anvil(cmd: str, username=_USERNAME_) -> str | list[str]:
    """Send a shell command to anvil and parse the output

    Args:
        cmd (str): the command to send to anvil
        username (str, optional): your anvil username. tries to parse your anvil username by default.

    Returns:
        str | list[str]: the output of the command (cleaned of color tags)
    """
    output = parse_shell_output(check_output(['ssh', f'{username}@anvil.rcac.purdue.edu', *cmd.split(' ')], stderr=DEVNULL).decode().splitlines())
    return output
async def anvil_async(cmd: str): 
    """Just an asynchronous version of the anvil command"""
    asyncio.to_thread(anvil, cmd)
def anvil_queue(username=_USERNAME_):
    """Send a squeue command to anvil to check on your runs""" 
    return anvil(f"squeue -u {username}")
qs = anvil_queue

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Decorators                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!== 
class AnvilJob:
    def __init__(self, queue_row: str, sep="DISTINCTSEPERATOR") -> None:
        self.sep = sep
        [
            jobid, username, account, name, nodes, cpus, time_limit, status, time
        ] = queue_row.split()
        self.jobid = int(jobid)
        self.username = str(username)
        self.account = str(account)
        self.name = str(name)
        self.nodes = int(nodes)
        self.cpus = int(cpus)
        self.time_limit = str(time_limit)
        self.status = str(status)
        self.time = str(time)

    def __repr__(self) -> str: return "-"*30 + f"\n{self.name}: {self.status}\n\t{self.time}/{self.time_limit}"

    # def update(self, input=True, iter=True):
    #     match input, iter:
    #         case True, True:
    #             x = anvil(f"cat /anvil/scratch/{self.username}/sims/{self.name}/input/input; echo {self.sep}; ls /anvil/scratch/{self.username}/sims/{self.name}/Output/Fields/Magnetic/Total/x/")
    #             input_lines = "\n".join(x).split(self.sep)[0].split('\n')
    #             self.input = dHybridRinput(input_lines)
    #             self.iter = int(x[-1][5:-3])
    #         case True, False:
    #             self.input = dHybridRinput(anvil(f"cat /anvil/scratch/{self.username}/sims/{self.name}/input/input"))
    #         case False, True:
    #             self.iter = int(anvil(f"ls /anvil/scratch/{self.username}/sims/{self.name}/Output/Fields/Magnetic/Total/x/")[-1][5:-3])
def get_anvil_jobs(username=_USERNAME_) -> list[AnvilJob]:
    """Parse the squeue and return AnvilJob objects"""
    q = anvil(f"squeue -u {username}")
    if type(q)==str: return []
    return [AnvilJob(x) for x in q[1:]]
async def get_anvil_jobs_async(username=_USERNAME_):
    """Just an asynchronous version of get_anvil_jobs"""
    q = await asyncio.to_thread(anvil, f"squeue -u {username}")
    if type(q)==str: return []
    return [AnvilJob(x) for x in q[1:]]
async def get_anvil_sim_iter(name: str, username=_USERNAME_):
    iter = int(await asyncio.to_thread(anvil, f"ls /anvil/scratch/{username}/sims/{name}/Output/Fields/Magnetic/Total/x/")[-1][5:-3])
    return iter
class AnvilQueue:
    def __init__(self, username=_USERNAME_):
        self.username = username
    @property
    def jobs(self): return get_anvil_jobs()
    def monitor(self, sep="DISTINCTSEPERATOR"):
        with redirect_to_tqdm():
            js = self.jobs
            print(js, self.jobs)
            pbars=[tqdm(position=i, leave=True, desc=js[i].name, postfix=f"{js[i].time}/{js[i].time_limit}") for i in range(len(js))]
            for i in range(len(js)):
                j = js[i]
                j.update()
                pbars[i].total = j.input.niter
                pbars[i].n = j.iter
                pbars[i].refresh()
            while len(js:=self.jobs) > 0:
                x = anvil(f";echo {sep};".join([f"ls /anvil/scratch/{self.username}/sims/{js[i].name}/Output/Fields/Magnetic/Total/x/" for i in range(len(js))]))
                sep_ind = 0
                for i in range(len(js)):
                    if i==range(len(js))[-1]: 
                        sep_ind=0
                    else: 
                        while x[sep_ind]!=sep: sep_ind+=1
                    it = int(x[sep_ind-1][5:-3])
                    pbars[i].n = it 
                    pbars[i].postfix = f"{js[i].time}/{js[i].time_limit}"
                    pbars[i].refresh()
                    sep_ind+=1
    def sound_when_running(self, i=0):
        while len(js:=self.jobs) > 0:
            j = js[i]
            if j.status=='R': return success()
    def sound_when_queue_clear(self):
        while len(js:=self.jobs)>0: sleep(20)
        return success()
    def sound_monitor(self):
        self.sound_when_running()
        self.sound_when_queue_clear()