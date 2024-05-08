import subprocess

def increase_volume():
    try:
        subprocess.run(['nircmd', 'changesysvolume', '2000'])
        print("音量已调大")
    except subprocess.CalledProcessError:
        print("调用nircmd失败")

def decrease_volume():
    try:
        subprocess.run(['nircmd', 'changesysvolume', '-2000'])
        print("音量已调小")
    except subprocess.CalledProcessError:
        print("调用nircmd失败")
