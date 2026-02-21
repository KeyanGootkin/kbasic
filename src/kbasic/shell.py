# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from kbasic.bar import ProgressBar, redirect_to_tqdm
from kbasic.audio import success
from kbasic.environment import isAnvil 
if isAnvil: from kbasic.environment.anvil import anvil_user
# from kgsim.dhybridr.io import dHybridRinput
from subprocess import check_output, DEVNULL
from tqdm import tqdm
from time import sleep
import asyncio
import numpy as np

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                              Types                              <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
bad = ['\x1b[31m', '\x1b[34m', '\x1b[m']
ansi = {"BLACK": u"\033[0;30m","RED": u"\x1b[0;31m","GREEN": u"\033[0;32m","BROWN": u"\033[0;33m","BLUE": u"\033[0;34m","PURPLE": u"\033[0;35m","CYAN": u"\033[0;36m","WHITE": u"\033[0;37m",
    "FAINT": u"\033[2m","FAINT BLACK": u"\033[2;30m","FAINT RED": u"\x1b[2;31m","FAINT GREEN": u"\033[2;32m","FAINT BROWN": u"\033[2;33m","FAINT BLUE": u"\033[2;34m","FAINT PURPLE": u"\033[2;35m","FAINT CYAN": u"\033[2;36m","FAINT WHITE": u"\033[2;37m",
    "ITALIC": u"\033[3m","ITALIC BLACK": u"\033[3;30m","ITALIC RED": u"\x1b[3;31m","ITALIC GREEN": u"\033[3;32m","ITALIC BROWN": u"\033[3;33m","ITALIC BLUE": u"\033[3;34m","ITALIC PURPLE": u"\033[3;35m","ITALIC CYAN": u"\033[3;36m","ITALIC WHITE": u"\033[3;37m",
    "UNDERLINE": u"\033[4m","UNDERLINE BLACK": u"\033[4;30m","UNDERLINE RED": u"\x1b[4;31m","UNDERLINE GREEN": u"\033[4;32m","UNDERLINE BROWN": u"\033[4;33m","UNDERLINE BLUE": u"\033[4;34m","UNDERLINE PURPLE": u"\033[4;35m","UNDERLINE CYAN": u"\033[4;36m","UNDERLINE WHITE": u"\033[4;37m",
    "BLINK": u"\033[5m","BLINK BLACK": u"\033[5;30m","BLINK RED": u"\x1b[5;31m","BLINK GREEN": u"\033[5;32m","BLINK BROWN": u"\033[5;33m","BLINK BLUE": u"\033[5;34m","BLINK PURPLE": u"\033[5;35m","BLINK CYAN": u"\033[5;36m","BLINK WHITE": u"\033[5;37m",
    "NEGATIVE": u"\033[7m","BLACK BACKGROUND": u"\033[7;30m","RED BACKGROUND": u"\x1b[7;31m","GREEN BACKGROUND": u"\033[7;32m","BROWN BACKGROUND": u"\033[7;33m","BLUE BACKGROUND": u"\033[7;34m","PURPLE BACKGROUND": u"\033[7;35m","CYAN BACKGROUND": u"\033[7;36m","WHITE BACKGROUND": u"\033[7;37m",
    "END": u"\033[0m"
}
_USERNAME_ = None if not isAnvil else anvil_user
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def pprint(text: str, option: str = 'white'):
    assert option.upper() in ansi.keys(), f"must give one of {ansi.keys()} as your option. "
    output = ansi[option.upper()] + text + ansi['END']
    print(output)
def warn(text: str): pprint(text, 'yellow')
def parse_shell_output(output):
        match output:
            case str(): return output 
            case [x]: return x
            case [x, *_]: 
                for i in range(len(output)):
                    for b in bad:
                        if b in output[i]:
                            output[i] = output[i].strip(b)
                return output
def system(cmd: str):
    print(cmd)
    command = cmd.split(' ') if type(cmd)==str else cmd
    print(command)
    for i in range(len(command)-1):
        if command[i].startswith('"'): 
            print(command[i])
            start_quote = i 
            end_quote = i+1
            while not command[end_quote].endswith('"'): end_quote+=1
            command[i] = " ".join(command[start_quote:end_quote+1])
            for j in range(start_quote+1, end_quote+1): del command[j]
    output = parse_shell_output(check_output(command, stderr=DEVNULL).decode().splitlines())
    return output
def anvil(cmd: str):
    output = parse_shell_output(check_output(['ssh', 'x-kgootkin@anvil.rcac.purdue.edu', *cmd.split(' ')], stderr=DEVNULL).decode().splitlines())
    return output
async def anvil_async(cmd: str): asyncio.to_thread(anvil, cmd)
def anvil_queue(username=_USERNAME_): return anvil(f"squeue -u {username}")
qs = anvil_queue

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Decorators                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!== 
class AnvilJob:
    def __init__(self, queue_row: str, sep="DISTINCTSEPERATOR"):
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

    def __repr__(self): return "-"*30 + f"\n{self.name}: {self.status}\n\t{self.time}/{self.time_limit}"

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
def get_anvil_jobs(username=_USERNAME_):
    q = anvil(f"squeue -u {username}")
    if type(q)==str: return []
    return [AnvilJob(x) for x in q[1:]]
async def get_anvil_jobs_async(username=_USERNAME_):
    q = await asyncio.to_thread(anvil, f"squeue -u {username}")
    if type(q)==str: return []
    return [AnvilJob(x) for x in q[1:]]
async def get_anvil_sim_iter(name: str):
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