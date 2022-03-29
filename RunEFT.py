import subprocess, multiprocessing, time, getopt, sys, os
__author__      = "Doomlad"
__copyright__   = "Copyright © 2022"
__version__     = "1.0.0-alpha"
__date__        = "03-27-2022"
def server_thread(server_executable, launcher_executable):
    server_ready = False
    try:
        server = subprocess.Popen(server_executable, stdout=subprocess.PIPE)
        for line in server.stdout:
            print(line.decode(), end='')
            if "Server is running" in line.decode() and not server_ready:
                server_ready = True
                print("[Starting launcher]", end='\r\b')
                server = subprocess.Popen(launcher_executable)
                time.sleep(2)
            print("[Waiting for server]", end='\r\b') if not server_ready else print("[Listening for client]", end='\r\b')
        return_code = server.wait()
        if return_code: raise subprocess.CalledProcessError(return_code, server_executable)
    except FileNotFoundError: 
        print("Error: File not found, please supply a valid path to your server/launcher executables.")
        os.system("pause")
def main():
    print(f"Escape from Tarkov - SPT AKI Auto-Launcher\nVersion: {__version__} {__copyright__} {__author__}")
    server_executable = "Server.exe"
    launcher_executable = "Launcher.exe"
    try:
        args, vals = getopt.getopt(sys.argv[1:], "hs:l:", ["help","server", "launcher"])
        for arg, val in args:
            if arg in ("-h", "--help"):
                print(f"\nusage: {sys.argv[0]} [-h] [-s] <server> [-l] <launcher>\nIf no options are provided, script uses default(s) \"Server.exe\" and \"Launcher.exe\"")
                exit()
            elif arg in ("-s", "--server"): server_executable = val
            elif arg in ("-l", "--launcher"): launcher_executable = val
    except getopt.error as err: 
        print(str(err))
        os.system("pause")
    server = multiprocessing.Process(target=server_thread, args=(server_executable, launcher_executable))
    server.start()
if __name__ == "__main__":
    main()
