def help_func(self, *args) -> str:
    menu = self.menu

    if menu == "MM":
        return "Main menu commands are:\n1, 2, 3, 4, 6"

    # Хардкод команд по меню
    if menu == "PM":
        SHORT_HELP = {
            "G826":"                      Display DSL G.826 parameter",
            "G826 C": "                    Display DSL G.826 continuously",
            "G826 E1": "                   Display E1 G.826 parameter",
            "G826 E1 C": "                 Display E1 G.826 continuously",
            "RESETG826 [ALL]": "           Reset G.826 parameters for entire DSL",
            "RESETG826": "                 Reset G.826 error performance parameters",
            "DATE [date] [ALL]": "         Set date",
            "DATE": "                      Get current date",
            "TIME [time] [ALL]": "         Set time",
            "TIME":"                      Get current time",
            "NETSTAT": "                   Display network interface statistics",
            "RESETNETSTAT [ALL]": "        Reset network interface statistics for DSL link",
            "RESETNETSTAT":"              Reset network interface statistics",
            "CONNECT [n]": "               Connect to remote unit; n=R",
            "DISCONNECT": "                Disconnect virtual terminal",
            "M": "                         Return to Main Menu, or previous level menu",
            "H [command]": "               Show help on command",
            "H": "                         Show available commands"
        }
        FULL_HELP = {
            "G826": "",
            "G826 C": "",
            "G826 E1": "",
            "G826 E1 C": "",
            "RESETG826": "",
            "DATE": "",
            "TIME": "",
            "NETSTAT": "",
            "RESETNETSTAT": "",
            "CONNECT": "",
            "DISCONNECT": "",
            "M": "",
        }
    elif menu == 'FMM':
        SHORT_HELP = {
            "SQ":"                        Turn signal quality trace on/off",
            "STARTUP":"                   Turn DSL transceiver startup trace on/off",
            "STATUS":"                    Display local system status",          
            "LOOP1 [E/N] [ON/OFF]":"      Local loopback on E1/Nx64 interface",
            "LOOP2 [n] [ON/OFF]":"        Set local DSL loopback; n=[L/R]",            
            "RESTART":"                   Reset local unit",         
            "CONNECT [n]":"               Connect to remote unit; n=R",
            "DISCONNECT":"                Disconnect virtual terminal",   
            "M":"                         Return to Main Menu, or previous level menu",        
        }
        FULL_HELP = {
            "SQ": "",
            "STARTUP": "",
            "STATUS": "",
            "LOOP1": "",
            "LOOP2": "",
            "RESTART": "",
            "CONNECT": "",
            "DISCONNECT": "",
            "RESETNETSTAT": "",
            "CONNECT": "",
            "DISCONNECT": "",
        }
    elif menu == "CM":
        SHORT_HELP = {
            "CONFIG":"                    Display local configuration",
            "HW":"                        Display hardware configuration",                
            "G704 [ON/OFF]":"             Set framed/transparent mode",            
            "CRC4 [ON/OFF]":"             Set CRC4 detection and generation mode",     
            "EBIT [ON/OFF]":"             Set automatic E-bit insertion",       
            "AISGEN [ON/OFF]":"           Set AIS generation",     
            "AISDET [ON/OFF]":"           Set AIS detection",
            "EXTCLK [ON/OFF]":"           Enable/disable external clock",
            "PCM [30/31] [C/T]":"         Enable/disable processing of signalling timeslot",               
            "IDLECAS [hex]":"             Set the idle pattern for signalling slot; hex=[0..F]",         
            "IDLEPAT [hex]":"             Set the idle pattern for data slot; hex=[0..FF]",     
            "SIGSLOTS [AUTO/a,e]":"       Set signaling slot numbers; a,e=[1..31]",           
            "SERVICE [I1..In]":"          Select interface(s) for transmit through DSL",              
            "TYPE [n]":"                  Set Nx64 interface type; n=[1..4]",              
            "BITRATE [n]":"               Set Nx64 payload data rate; n=[1..36]",
            "CLOCKDIR [CO/CONTRA]":"      Set Nx64 clock direction: Co- or Contradirectional",
            "CLOCKMODE [EXT/INT]":"       Set Nx64 clock mode: external;int",
            "SLOTUSAGE [ON/OFF]":"        Set usage of DSL timeslot 0",    
            "MASTER [ON/OFF]":"           Set CO/CPE mode",         
            "PLL [ON/OFF]":"              Set PLL of channel A",                
            "POWER [ON/OFF]":"            Enable power",         
            "RS232SLOT [n]":"             Set RS232 timeslot number: n=[1..35]",   
            "RS232BITS [n]":"             Set number of RS232 data bits; n=[7..10]",
            "RS232RATE [n]":"             Set RS232 rate; n=[110..115200]",
            "RS232ERATE [n]":"            Set RS232 excess rate; n=[1..5]", 
            "AUTORST [ON/OFF]":"          Set DSL autorestart",        
            "BASERATE [n]":"              Set Nx64 baserate; n=[3..36]",   
            "ADAPT [ON/OFF]":"            Set adaptation mode",             
            "SCALE":"                     Set output TX power offset; n=[-16..+2]",
            "DEFAULT [n]":"               Set default configuration; n=[0..5]",         
            "ID [text]":"                 Set ID string (up to 20 characters)",              
            "ETHSD [10/100/AUTO] [H/F]":" HW set ethernet speed or speed auto negotiation",            
            "ETHPAYLOAD [n]":"            Set number of DSL slots for Ethernet data flow", 
            "CONNECT [n]":"               Connect to remote unit; n=R",
            "DISCONNECT":"                Disconnect virtual terminal",   
            "M":"                         Return to Main Menu, or previous level menu",
            "H [command]":"               Show help on command",
            "H":"                         Show available commands",
        }
        FULL_HELP = {
            "CONFIG": "",
            "HW": "",
            "G704": "",
            "CRC4": "",
            "EBIT": "",
            "AISGEN": "",
            "AISDET": "",
            "EXTCLK": "",
            "PCM": "",
            "IDLECAS": "",
            "IDLEPAT": "",
            "SIGSLOTS": "",
            "SERVICE":"",
            "TYPE":"",
            "BITRATE":"",
            "CLOCKDIR":"",
            "CLOCKMODE":"",
            "SLOTUSAGE":"",
            "MASTER":"",
            "PLL":"",
            "POWER":"",
            "RS232SLOT":"",
            "RS232BITS":"",
            "RS232RATE":"",
            "RS232ERATE":"",
            "AUTORST":"",
            "BASERATE":"",
            "ADAPT":"",
            "SCALE":"",
            "DEFAULT":"",
            "ID":"",
            "ETHSD":"",
            "ETHPAYLOAD":"",
            "CONNECT":"",
            "DISCONNECT":"",
        }

    if len(args) == 0:
        output = ["----------------------------------------------------------------------"]
        for cmd in SHORT_HELP.keys():
            output.append(f"{cmd}: {SHORT_HELP[cmd]}")
        return "\n".join(output)

    else:
        cmd = " ".join(args).upper()
        if cmd in FULL_HELP:
            return FULL_HELP[cmd]
        else:
            return "Illegal parameter(s)!\n"
