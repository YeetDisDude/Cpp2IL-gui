import os, subprocess

modules = [
    ("dearpygui", "import dearpygui.dearpygui as dpg"),
    ("httpx", "import httpx"),
    ("requests", "import requests"),
    ("tkinter", "from tkinter import Tk"),
]

needed = []
for module, import_string in modules:
    try:
        exec(import_string)
    except ImportError:
        needed.append(module)

if len(needed) != 0:
    count = 0
    for module in needed:
        count += 1
        print(f"[i] Installing Required Modules... | {count} / {len(needed)}")
        subprocess.check_call(["pip3", "install", module, "-q"])

import dearpygui.dearpygui as dpg
import httpx
import json
from tkinter import Tk
from tkinter.filedialog import askopenfile, askdirectory

filepath = os.path.abspath(__file__)
filename = os.path.basename(__file__)
folderpath = os.getcwd()

commands = []
VERSION = "0.1.0"
UPDATE_URL = "https://raw.githubusercontent.com/YeetDisDude/Cpp2IL-gui/main/version.txt"

cpp2ilcmds = {
    "Game Path": "Path to the APK",
    "Analysis Level": "cpp2il_out/types/[Assembly]/typename_methods.txt",
    "Skip Analysis": "only generate Dummy DLLs and optionally metadata dumps",
    "Skip Metadata txts": "Flag to skip metadata dumps (cpp2il_out/types/[Assembly]/typename_metadata.txt)",
    "Disable Registration prompts": "Flag to prevent asking for the user to input addresses in STDIN if they can't be detected",
    "Verbose": "Log more information about what we are doing",
    "IL to Assembly": "Attempt to save generated IL to the DLL file where possible. MAY BREAK THINGS.",
    "Suppress Attributes": "Prevents generated DLLs from containing attributes providing il2cpp-specific metadata, such as function pointers, etc.",
    "Parallel": "Run analysis in parallel. Usually much faster, but may be unstable. Also puts your CPU under a lot of strain (100% usage is targeted).",
    "Run analysis for asm": "Do not specify the .dll extension.",
    "Throw safety out the window": "Do not abort attempting to generate IL for a method if an error occurs. Instead, continue on with the next action, skipping only the one which errored. WILL PROBABLY BREAK THINGS.",
    "Analyze All": "Analyze all assemblies in the application",
    "Skip Method Dumps": "Suppress creation of method_dumps folder and files",
    "Just give me DLLs": "Shorthand for --parallel --skip-method-dumps --experimental-enable-il-to-assembly-please --throw-safety-out-the-window --skip-metadata-txts",
    "Simple Attribute Restoration": "Don't use analysis to restore attributes"
}

def check_update():
    dpg.set_value(f"updatetxt", "Update Status: Checking for updates...")
    r = httpx.get(UPDATE_URL)
    if r.text.strip() != VERSION:
        dpg.set_value("updatetxt", f"Update Status: Version {VERSION} is Outdated! Download the latest version from github.com/YeetDisDude/Cpp2IL-GUI")
    else:
        dpg.set_value(f"updatetxt", f"Update Status: Cpp2IL Gui version {VERSION} is up to date!")
    


def modify_commands(cmdtype: bool, command: str):
    command = command.strip()
    if cmdtype:
        commands.append(command); print(commands)
        dpg.set_value("cmdslist", commands)
    else:
        commands.remove(command); print(commands)
        dpg.set_value("cmdslist", commands)

def addanalysislevel(level):
    for i, command in enumerate(commands):
        if command.startswith('--analysis-level='):
            commands[i] = f'--analysis-level="{level}"'; print(commands)
            dpg.set_value("cmdslist", commands)
            return
    commands.append(f'--analysis-level="{level}"'); print(commands)
    dpg.set_value("cmdslist", commands)

def list_to_args(lst: list):
    return " ".join(lst)

def addgamepath(path: str):
    apkpath = path.strip()
    dpg.set_value("cmdslist", commands)
    for i, command in enumerate(commands):
        if command.startswith('--game-path='):
            commands[i] = f'--game-path="{apkpath}"'; print(commands)
            dpg.set_value("cmdslist", commands)
            return
    commands.append(f'--game-path="{apkpath}"'); print(commands)
    dpg.set_value("cmdslist", commands)

def addoutputpath(path: str): # not used rn
    outputpath = path.strip()
    dpg.set_value("cmdslist", commands)
    for i, command in enumerate(commands):
        if command.startswith('--output-to='):
            commands[i] = f'--output-to="{outputpath}"'; print(commands)
            dpg.set_value("cmdslist", commands)
            return
    commands.append(f'--output-to="{outputpath}"'); print(commands)
    dpg.set_value("cmdslist", commands)


def selectapk():
    Tk().withdraw()
    try:
        file_path = askopenfile(filetypes=[("APK Files", "*.apk")])
        if file_path:
            apk_name = file_path.name.split("/")[-1] # get the name of the file
            print(f"Selected APK: {apk_name}")
            dpg.set_value("selectedapk", f"Selected APK: {apk_name}")
            addgamepath(file_path.name)
        print(f"File path: {file_path.name}")
    except AttributeError:
        print("[ERROR] No file selected")

def outputto():
    Tk().withdraw()
    folder_path = askdirectory()
    print(f"Selected Output Directory: {folder_path}")
    dpg.set_value("selectedoutput", f"Selected Output: {folder_path}")
    addoutputpath(folder_path)

def analysislevel():
    analysislevel = dpg.get_value("analysisleveltag")
    if analysislevel <= 0:
        analysislevel = 0
        dpg.set_value("analysisleveltag", analysislevel)
    elif analysislevel >= 4:
        analysislevel = 4
        dpg.set_value("analysisleveltag", analysislevel)
    print(f"Analysis Level: {analysislevel}")
    addanalysislevel(str(analysislevel))

def skipanalysis():
    isskipanalysis = dpg.get_value("skipanalysistag")
    print(f"Skip analysis: {isskipanalysis}")
    modify_commands(isskipanalysis, "--skip-analysis")

def skipmetadatatxts():
    isskipmetadatatxts = dpg.get_value("skipmetadatatxtstag")
    print(f"Skip Metadata txts: {isskipmetadatatxts}")
    modify_commands(isskipmetadatatxts, "--skip-metadata-txts")

def disableregprompts():
    isdisableregprompts = dpg.get_value("disableregpromptstag")
    print(f"Disable reg Prompts: {isdisableregprompts}")
    modify_commands(isdisableregprompts, "--disable-registration-prompts")

def verbose():
    isverbose = dpg.get_value("verbosetag")
    print(f"Verbose: {isverbose}")
    modify_commands(isverbose, "--verbose")

def iltoasm():
    isiltoasm = dpg.get_value("iltoasmtag")
    print(f"IL to Asm: {isiltoasm}")
    modify_commands(isiltoasm, "--experimental-enable-il-to-assembly-please")

def suppressattributes():
    issuppressattributestag = dpg.get_value("suppressattributestag")
    print(f"Suppress Attributes: {issuppressattributestag}")
    modify_commands(issuppressattributestag, "--suppress-attributes")

def runanalysisforasm():
    isrunanalysisforasmtag = dpg.get_value("runanalysisforasmtag")
    print(f"Run analysis for Assembly: {isrunanalysisforasmtag}")
    modify_commands(isrunanalysisforasmtag, "--run-analysis-for-assembly")

def throwsafetyoutofwindow():
    isthrowsafetyoutofwindow = dpg.get_value("throwsafetyoutofwindowtag")
    print(f"Throw Safety Out of Window: {isthrowsafetyoutofwindow}")
    modify_commands(isthrowsafetyoutofwindow, "--throw-safety-out-the-window")

def analyzeall():
    isanalyzeall = dpg.get_value("analyzealltag")
    print(f"Analyze All: {isanalyzeall}")
    modify_commands(isanalyzeall, "--analyze-all")

def skipmethoddumps():
    isskipmethoddumps = dpg.get_value("skipmethoddumpstag")
    print(f"Skip Method Dumps: {isskipmethoddumps}")
    modify_commands(isskipmethoddumps, "--skip-method-dumps")

def parallel():
    isparallel = dpg.get_value("paralleltag")
    print(f"Parallel: {isparallel}")
    modify_commands(isparallel, "--parallel")

def givemealldlls():
    isgivemealldlls = dpg.get_value("givemealldllstag")
    print(f"Just Give me All DLLs: {isgivemealldlls}")
    modify_commands(isgivemealldlls, "--just-give-me-dlls-asap-dammit")

def simpleattributeres():
    issimpleattributeres = dpg.get_value("simpleattributerestag")
    print(f"Simple Attribute Restoration: {issimpleattributeres}")
    modify_commands(issimpleattributeres, "--simple-attribute-restoration")



def startcpp2il():
    arguments = list_to_args(commands)
    dpg.set_value("statustxt", "Running Cpp2IL...")
    print(f"Expected Cpp2IL Path: Cpp2IL")
    print(F"Cpp2IL arguments: {arguments}\n\n")

    exitcode = os.system(f'Cpp2IL\Cpp2IL.exe {arguments}')

    print(f"Finished running Cpp2IL... Exit Code: {exitcode}")
    if exitcode == -1: # cpp2il invalid arguments exit code
        dpg.set_value("statustxt", "Error:   Invalid arguments given to Cpp2IL")
    elif exitcode == 1: # could not find file exit code
        dpg.set_value("statustxt", "Error:   Could not find Cpp2IL.exe!")
    else:
        dpg.set_value("statustxt", "An unknown error occured.")

def tab1(): # main page
    with dpg.group():
        dpg.bind_font(default_font)
        dpg.add_text(" ")
        dpg.add_button(label="Select a file", callback=selectapk, width=150, height=25)
        dpg.add_text("Selected file: ", tag="selectedapk")
        dpg.add_text(" ")
        # dpg.add_button(label="Output to", width=150, height=25, callback=outputto)
        # dpg.add_text("Selected Output: ", tag="selectedoutput")
        # dpg.add_text(" ")

        dpg.add_separator()

        dpg.add_slider_int(label="  Analysis Level                     ", width=150, min_value=0, max_value=4, callback=analysislevel, tag="analysisleveltag", default_value=-1) # --analysis-level
        dpg.add_checkbox(label="  Skip  Analysis                       ", tag="skipanalysistag", callback=skipanalysis) # --skip-analysis
        dpg.add_checkbox(label="  Skip  Metadata  Texts                ", tag="skipmetadatatxtstag", callback=skipmetadatatxts) # --skip-metadata-txts
        dpg.add_checkbox(label="  Disable  Registration  Prompts       ", tag="disableregpromptstag", callback=disableregprompts) # --disable-registration-prompts
        dpg.add_checkbox(label="  Verbose [Recommended]                ", tag="verbosetag", callback=verbose) # --verbose
        dpg.add_checkbox(label="  IL  to  Assembly  ( Experimental )   ", tag="iltoasmtag", callback=iltoasm) # --experimental-enable-il-to-assembly-please
        dpg.add_checkbox(label="  Suppress  Attributes                 ", tag="suppressattributestag", callback=suppressattributes) # --suppress-attributes
        dpg.add_checkbox(label="  Run  Analysis  for  Assembly         ", tag="runanalysisforasmtag", callback=runanalysisforasm) # --run-analysis-for-assembly
        dpg.add_checkbox(label="  Throw  Safety  Out  of  Window       ", tag="throwsafetyoutofwindowtag", callback=throwsafetyoutofwindow) # --throw-safety-out-the-window	
        dpg.add_checkbox(label="  Analyze  All                         ", tag="analyzealltag", callback=analyzeall) # --analyze-all	
        dpg.add_checkbox(label="  Skip  Method  Dumps                  ", tag="skipmethoddumpstag", callback=skipmethoddumps) # --skip-method-dumps
        dpg.add_checkbox(label="  Parallel                             ", tag="paralleltag", callback=parallel) # --parallel	
        dpg.add_checkbox(label="  Just  Give  me  DLLs  Asap           ", tag="givemealldllstag", callback=givemealldlls) # --just-give-me-dlls-asap-dammit
        dpg.add_checkbox(label="  Simple  Attribute  Restoration       ", tag="simpleattributerestag", callback=simpleattributeres) # --simple-attribute-restoration
        dpg.add_input_text(label="Commands", readonly=True, tag="cmdslist")
        dpg.add_text(" ")
        dpg.add_button(label="Start", callback=startcpp2il, width=150, height=50)
        dpg.add_text("Status: idle", tag="statustxt")


def tab2(): # cpp2il documentation
    with dpg.group():
        dpg.add_text(" ")
        with dpg.table(header_row=False, row_background=True,
                    borders_innerH=True, borders_outerH=True, borders_innerV=True,
                    borders_outerV=True):
            dpg.add_table_column()
            dpg.add_table_column()
            with dpg.table_row():
                dpg.add_text("Option")
                dpg.add_text("Description")
            for key, value in cpp2ilcmds.items():
                with dpg.table_row():
                    for i in range(0, 2):
                        dpg.add_text(key)
                        dpg.add_text(value)
            


def tab3(): # credits
    with dpg.group():
        dpg.add_text("Credits")
        dpg.add_text(" ")
        dpg.add_text("Samboy - For Cpp2IL | github.com/SamboyCoding")
        dpg.add_text("github.com/SamboyCoding/Cpp2IL")

def tabsetting(): # settings
    with dpg.group():
        dpg.add_text(" ")
        dpg.add_button(label="Check update", callback=check_update, width=150, height=50)
        dpg.add_text("Update Status: idle", tag="updatetxt")
        dpg.add_text(" ")
        dpg.add_text("Current Cpp2IL version: 2022.0.7")


imguiW = 800
imguiH = 500


dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()
dpg.set_viewport_width(imguiW + 16)
dpg.set_viewport_height(imguiH + 38)
dpg.set_viewport_resizable(False)




with dpg.font_registry():
    default_font = dpg.add_font("Assets/SF Pro Display Semibold.ttf", 20)

with dpg.window(width=imguiW, height=imguiH, no_resize=True, label=f"Cpp2IL Gui | Made by: YeetDisDude#0001 | Version {VERSION}") as window:
    with dpg.tab_bar():
        with dpg.tab(label="     Cpp2IL     "):
            tab1()
        with dpg.tab(label="     CPP2IL  Documentation     "):
            tab2()
        with dpg.tab(label="    Credits     "):
            tab3()
        with dpg.tab(label="    Settings     "):
            tabsetting()


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()