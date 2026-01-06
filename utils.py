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
            "G826": (
                "SYNTAX: G826 or G\n"
                "This command displays the ITU-T G.826 error performance on the DSL line side.\n"
                "CRC6                          : Cyclic redundancy check indicating errored\n"
                "                                blocks detected locally\n"
                "FEBE                          : Far end block error indicating errored blocks\n"
                "                                detected on the remote unit\n"
                "Errored block (EB)            : a block in which one or more bits are in error\n"
                "Errored seconds (ES)          : a one second period with one or more\n"
                "                                errored blocks\n"
                "Severely errored second (SES) : a one second period which contains\n"
                "                                >=30 percent errored blocks\n"
                "Background block error (BBE)  : an errored block not occuring\n"
                "Available time                : a count of one second periods for which the DSL\n"
                "                                line is available.\n"
                "Unavailable time              : a count of one second periods for which the DSL\n"
                "                                line is unavailable.\n"

            ),
            "G826 C": (
                "SYNTAX: G826 C or G C\n"
                "This command displays the ITU-T G.826 error performance on the DSL line side\n"
                "continuously. See 'G826' for more information."
            ),
            "G826 E1": (
                "SYNTAX: G826 E1 or G E1\n"
                "This command displays the ITU-T G.826 error performance parameters on the\n"
                "E1 2Mbit/s side. This command is only available if framed mode is enabled.\n"
                "CRC4                          : Cyclic redundancy check indicating errored\n"
                "                                sub-multiframes detected locally\n"
                "E-Bit                         : CRC-4 indication bit indicating errored\n"
                "                                sub-multiframes detected on the remove unit\n"
                "FAS                           : signal detected locally"
                "Errored block (EB)            : a block in which one or more bits are in error\n"
                "Errored seconds (ES)          : a one second period with one or more\n"
                "                                errored blocks\n"
                "Severely errored second (SES) : a one second period which contains\n"
                "                                >=30 percent errored blocks\n"
                "Background block error (BBE)  : an errored block not occuring\n"
                "                                as part of an SES\n"
                "Available time                : a count of one second periods for which the E1\n"
                "                                interface is available.\n"
                "Unavailable time              : a count of one second periods for which the E1\n"
                "                                interface is unavailable.\n"

            ),
            "G826 E1 C": (
                "SYNTAX: G826 E1 C or G E1 C\n"
                "This command displays the ITU-T G.826 error perfomance parameters on the\n"
                "E1 2Mbit/s side continuously. See 'G826 E1' for more information."
            ),
            "RESETG826": (
                "SYNTAX: RESETG826 [ALL] or RG [ALL]\n"
                "This command resets all G.826 error performance parameters back to zero.\n"
                "If 'ALL' parameter used, this command resets G.826 error performance\n"
                "parameters in all devices of DSL link."
            ),
            "DATE": (
                "SYNTAX: DATE [date] [ALL] or DA [date] [ALL]\n"
                "This command without parameter displays current date.\n"
                "This command with parameter sets DD/MM/YYYY date.\n"
                "If 'ALL' parameter used, this command sets date in all devices of DSL link."
            ),
            "TIME": (
                "SYNTAX: TIME [time] [ALL] or TI [time] [ALL]\n"
                "This command without parameter displays current time.\n"
                "This command with parameter HH:MM:SS sets time.\n"
                "If 'ALL' parameter used, this command sets time in all devices of DSL link."
            ),
            "NETSTAT": (
                "SYNTAX: NETSTAT or NETS\n"
                "This command displays statistics of Ethernet connection.\n"
                "Bytes transmitted   : number of bytes sent via network interface.\n"
                "Packets transmitted : number of packets sent via network interface.\n"
                "Bytes received      : number of bytes received via network interface.\n"
                "Packets received    : number of packets received via network interface.\n"
                "Errors              : number of errors occured during transmission via network\n"
                "                      interface.\n"
                "Collisions          : number of collisions detected on network interface.\n"
                "Available time      : number of seconds network interface was up.\n"
                "Unavailable time    : number of seconds network interface was down."
            ),
            "RESETNETSTAT": (
                "SYNTAX: RESETNETSTAT [ALL] or RNS [ALL]\n"
                "This command resets all statistics that are displayed by command NETSTAT.\n"
                "If 'ALL' parameter used, this command resets all statistics in all devices\n"
                "of DSL link."
            ),
            "CONNECT": (
                "SYNTAX: CONNECT [n] or CO [n]\n"
                "This command opens a virtual terminal connection to the remote unit, i.e.\n"
                "characters received at the local unit's V.24 interface (keyboard messages) are\n"
                "send to the remote unit, and characters sent from the remote unit (screen\n"
                "messages) are transmitted back to the local unit's V.24 interface.\n"
                "During a virtual terminal session, the local unit is not available any more,\n"
                "unless you close your session by typing the DISCONNECT command or by selecting\n"
                "'Exit' on the main menu screen of the session.\n"
                "R    : Remote unit selected\n"
                "1..13: Regenerator number 1 to 13 selected"
            ),
            "DISCONNECT": (
                "SYNTAX: Disconnect or DIS\n"
                "This command closes an open virtual terminal connection to the remote unit."
            ),
            "M": (
                "SYNTAX: M\n"
                "Return to main menu, or previous level menu."
            ),
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
            "SQ": (
                "SYNTAX: SQ\n"
                "This command toggles the signal quiality trace on and off.\n"
                "SNR is the ratio of constellation power to equalizer error power.\n"
                "The equalizer error is the distance from the receive constellation point\n"
                "to the closest constellation point. The constellation power is\n"
                "proportional to the average of the square of the distance of each\n"
                "transmitted constellation point from the origin."
            ),
            "STATUS": (
                "SYNTAX: STATUS or ST\n"
                "This command displays the actual system status.\n"
                "LOSD        : Loss of signal\n"
                "SEGA        : Segment anomaly\n"
                "PS          : Power status\n"
                "SEGD        : Segment defect\n"
                "Tx power    : Local transmit power in dBm\n"
                "Rx gain     : Local receiver gain in dB\n"
                "Loop attn.  : Estimate of the loop attenuation in dB\n"
                "SNR         : Current signal quality in dB\n"
                "Bitrate     : DSL Bitrate of the actual connection\n"
                "SRU         : Number of detected repeater in loop"
            ),
            "STARTUP": (
                "SYNTAX: STARTUP or SUP\n"
                "This command toggles the startup trace on and off, in order to observer the\n"
                "activation state diagram transitions conforming to ITU-T G.991.2."
            ),
            "LOOP1": (
                "SYNTAX: LOOP1 [E/N] [ON/OFF] or L1 [E/N] [ON/OFF]\n"
                "This command starts/stops the local loopback at the subscriber interface.\n"
                " E    : Local loopback for E1 interface\n"
                " N    : Local loopback for Nx64 interface\n"
            ),
            "LOOP2": (
                "SYNTAX: LOOP2 [n] [ON/OFF] or L2 [n] [ON/OFF]\n"
                "This command starts/stops the loopback at local unit; n=[L/R].\n"
                "L    : Local unit selected\n"
                "R    : Remote (master) unit selected"
            ),
            "RESTART": (
                "SYNTAX: RESTART or RE\n"
                "This command restarts the link of the actual channel."
            ),
            "CONNECT": (
                "SYNTAX: CONNECT [n] or CO [n]\n"
                "This command opens a virtual terminal connection to the remote unit, i.e.\n"
                "characters received at the local unit's V.24 interface (keyboard messages) are\n"
                "send to the remote unit, and characters sent from the remote unit (screen\n"
                "messages) are transmitted back to the local unit's V.24 interface.\n"
                "During a virtual terminal session, the local unit is not available any more,\n"
                "unless you close your session by typing the DISCONNECT command or by selecting\n"
                "'Exit' on the main menu screen of the session.\n"
                "R    : Remote unit selected\n"
                "1..13: Regenerator number 1 to 13 selected"
            ),
            "DISCONNECT": (
                "SYNTAX: Disconnect or DIS\n"
                "This command closes an open virtual terminal connection to the remote unit."
            ),
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
            "CONFIG": (
                "SYNTAX: CONFIG or C\n"
                "This command displays the actual configuration of the unit."
            ),
            "HW": (
                "SYNTAX: HW\n"
                "This command displays the actual hardware configuration of the unit."
            ),
            "G704": (
                "SYNTAX: G704 [ON/OFF]\n"
                "This command selects between E1 transparent and framed mode according to G.704."
            ),
            "CRC4": (
                "SYNTAX: CRC4 [ON/OFF] or C4 [ON/OFF]\n"
                "This command enables (ON)/disables (OFF) CRC-4 processing:\n"
                "   ON:  1) The E1 framer will synchronize on CRC4 multiframes and\n"
                "        CRC4 errors (detected in the incoming stream) will be reported;\n"
                "        2) The E1 framer regenerates the CRC4 multiframe alignment and\n"
                "        checksum words in the outgoing E1 signal. The A-Bit is set to 0 and\n"
                "        the national bits (Sa-Bits) fully transparent (except Multipoint mode).\n"
                "   OFF: Timeslot 0 passes transparently from the DSL line towards the\n"
                "        E1 interface."
            ),
            "EBIT": (
                "SYNTAX: EBIT [ON/OFF] or E [ON/OFF]\n"
                "This command enables/disables automatic generation of E-Bits.\n"
                "ON : Detected CRC-4 errors will cause the assertion of the E-Bits\n"
                "OFF: All E-Bits are set to '1'"
            ),
            "AISGEN": (
                "SYNTAX: AISGEN [ON/OFF] or AG [ON/OFF]\n"
                "This command affects the behaviour of the transmitted data towards the E1\n"
                "interface if the DSL link is not established or the AIS-R alarm is active.\n"
                "ON : An unframed all '1's (AIS) will be transmitted on the E1 side\n"
                "OFF: No signal will be transmitted on the E1 side."
            ),
            "AISDET": (
                "SYNTAX: AISDET [ON/OFF] or AD [ON/OFF]\n"
                "This command enables/disables the detection of incoming AIS from the E1\n"
                "interface. If enabled, the AIS-S alarm on the local unit and AIS-R on the\n"
                "remote unit will be set upon detection of incoming AIS."
            ),
            "EXTCLK": (
                "SYNTAX: EXTCLK [ON/OFF]\n"
                "This command enables/disables the use of an external 2048 kHz clock source\n"
                "towards the DSL line. It is available on the master unit only.\n"
                "If this option is enabled, the primary E1 clock source is the external clock.\n"
                "If no external clock is present at the external clock input, the E1 transmit\n"
                "clock is used as the clock source. If no signal is received at the E1 port,\n"
                "then the internal clock is ued as the clock source."
            ),
            "PCM": (
                "SYNTAX: PCM [30/31] [C/T]\n"
                "This command enables/disables processing of signalling timeslot.\n"
                "[31]: Set signalling timeslot processing off.\n"
                "[30]: Set signalling timeslot processing on. If second parameter is C then\n"
                "      signalling slot is used for CAS signalization. If second parameter is T\n"
                "      then s\n"
                "      Signalling slot is transmitted transparently."
            ),
            "IDLECAS": (
                "SYNTAX: IDLECAS [hex] or IC [hex]\n"
                "This command sets the idle pattern (1..F) for signalling timeslot."
            ),
            "IDLEPAT": (
                "SYNTAX: IDLEPAT [hex] or IDP [hex]\n"
                "This command sets the idle pattern (0..FF) for unused data slot(s)."
            ),
            "SIGSLOTS": (
                "SYNTAX: SIGSLOTS [AUTO/a,e] or SS [AUTO/a,e]\n"
                "This command sets signalling slot numbers for DSL A and E1 interface.\n"
                " AUTO - automatic selection of signaling slot;\n"
                " a    - signaling slot number [1..31] for DSL A;\n"
                " e    - signaling slot number [1..31] for E1/G.703."
            ),
            "SERVICE":(
                "SYNTAX: SERVICE [I1..In] or SRV [I1..In]\n"
                "This command selects one or several interfaces and their order for transmitting\n"
                "through DSL. Available interfaces:\n"
                " E:   E1 interface\n"
                " N:   Nx64 interface\n"
                " ETH: Ethernet interface"
            ),
            "TYPE":(
                "SYNTAX: TYPE [n] or TP [n]\n"
                "This command sets the Nx64 interface type.\n"
                "0: V.35\n"
                "1: V.11 (V.36/X.21) without termination\n"
                "2: V.11 (V.36/X.21) with termination\n"
                "3: V.28 synchronous\n"
                "4: RS-232 asynchronous"
            ),
            "BITRATE":(
                "SYNTAX: BITRATE [n] or BTR [n]\n"
                "This command sets the Nx64 payload bit rate to [1..36] x 64 kbit/s for\n"
                "V.35 and V.11 or [1..2] x 64kbit/s for V.28."
            ),
            "CLOCKDIR":(
                "SYNTAX: CLOCKDIR [CO/CONTRA] or CD [CO/CONTRA]\n"
                "This command sets the Nx64 port clock direction to co- or contradirectional.\n"
                "CO    : Codirectional uses input line 113 for input data (103) sampling\n"
                "CONTRA: Contradirectional uses output line 114 for input data (103) sampling"
            ),
            "CLOCKMODE":(
                "SYNTAX: CLOCKMODE [EXT/INT] or CM [EXT/INT]\n"
                "This command selects wherefrom the clock towards the DSL line is derived\n"
                "when service Nx64 only is selected.\n"
                "EXT: External, i.e derived from the Nx64 input clock\n"
                "INT: Internal, i.e derived from the internal oscillator"
            ),
            "SLOTUSAGE":(
                "SYNTAX: SLOTUSAGE [ON/OFF] or SU [ON/OFF]\n"
                "This command enables/disables the usage of DSL timeslot 0.\n"
                "Timeslot 0 can be used:\n"
                "- for Ethernet payload\n"
                "- for Nx64 payload (excluding Nx64 type RS232)\n"
                "If E1 interface enabled, DSL timeslot 0 used to transmit timeslot 0 of E1.\n"
            ),
            "MASTER":(
                "SYNTAX: MASTER [ON/OFF] or MA [ON/OFF]\n"
                "This command selects the DSL master/slave mode.\n"
                "One unit must be configured as master, the other as slave."
            ),
            "PLL":(
                "SYNTAX: PLL [ON/OFF]\n"
                "This command enables/disables the PLL on channel A of DSL port."
            ),
            "POWER":(
                "SYNTAX: POWER [ON/OFF] or PW [ON/OFF]\n"
                "This command enable/disable remote power\n"
                "ON : remote power on in channel\n"
                "OFF: remote power off in channel\n"
            ),
            "RS232SLOT":(
                "SYNTAX: RS232SLOT [n] or RSS [n]\n"
                "This command assign timeslot n=[1..35] for RS232 transmission."
            ),
            "RS232BITS":(
                "SYNTAX: RS232BITS [n] or RSB [n]\n"
                "This command sets number the RS232 data bits n=[7..10]"
            ),
            "RS232RATE":(
                "SYNTAX: RS232RATE [n] or RSR [n]\n"
                "This command sets the RS232 receiver rate.\n"
                "Receiver rate n=[110/150/300/600/1200/2400/4800/9600/14400/19200/28800/38400\n"
                "                 /57600/115200]"
            ),
            "RS232ERATE":(
                "SYNTAX: RS232ERATE [n] or RSER [n]\n"
                "This command sets the excess rate RS232.\n"
                "n : excess rate of transmitter over receiver [1..4]\n"
                "    1 - 0 percent\n"
                "    2 - 0.5 percent\n"
                "    3 - 1 percent\n"
                "    4 - 2 percent\n"
                "    5 - 4 percent"
            ),
            "AUTORST":(
                "SYNTAX: AUTORST [ON/OFF] or AR [ON/OFF]\n"
                "This command enables/disables restarting the DSL channel.\n"
                "ON : The DSL channel restarts automatically\n"
                "OFF: The DSL channel does not restart - no startup occurs"
            ),
            "BASERATE":(
                "SYNTAX: BASERATE [n] or BR [n]\n"
                "This command sets the base DSL payload rate. This value defines the available\n"
                "64 kbit/s channels and must be between 3 and 36 for synchronous operation\n"
                "(PLL OFF) or between 3 and 32 for plesiochronous operation (PLL ON)."
            ),
            "ADAPT":(
                "SYNTAX: ADAPT [ON/OFF] or ADP [ON/OFF]\n"
                "This command enables/disables rate adaption during startup.\n"
            ),
            "SCALE":(
                "SYNTAX: SCALE [n] or SC [n]\n"
                "This command sets output TX power offset from ITU-T value in dBm.\n"
                "Parameter must be in the range [-16.0..2.0] with 0.5 dBm increment.\n"
                "For standard operation SCALE value must be set to 0.0 dBm."
            ),
            "DEFAULT":(
                "SYNTAX: DEFAULT [n] or DF [n]\n"
                "This command sets default configuration.\n"
                "There are two default configurations for multipoint mode (n=0..1),\n"
                "and six for all other modes (n=0..5)"
            ),
            "ID":(
                "SYNTAX: ID [text]\n"
                "This command sets a unique identification string printed on the main screen.\n"
                "This command without parameter clears the identification string."
            ),
            "ETHSD":(
                "SYNTAX: ETHSD [10/100/AUTO] [H/F] or SD [10/100/AUTO] [H/F]\n"
                "This command sets speed and duplex of Ethernet connection.\n"
                "ETHSD 10 H - set 10 MBit/s half duplex,\n"
                "ETHSD 10 F - set 10 Mbit/s full duplex,\n"
                "ETHSD 100 H - set 100 Mbit/s half duplex,\n"
                "ETHSD 100 F - set 100 Mbit/s full duplex,\n"
                "ETHSD AUTO  - set autonegotiation mode, when devices over Ethernet connection\n"
                "              try to determine speed and duplex automatically"
            ),
            "ETHPAYLOAD":(
                "SYNTAX: ETHPAYLOAD [n] or EPL [n]\n"
                "This command sets n - number of DSL slots for Ethernet data flow.\n"
                "Number of DSL slots for Ethernet data flow must not exceed number of available\n"
                "DSL slots."
            ),
            "CONNECT": (
                "SYNTAX: CONNECT [n] or CO [n]\n"
                "This command opens a virtual terminal connection to the remote unit, i.e.\n"
                "characters received at the local unit's V.24 interface (keyboard messages) are\n"
                "send to the remote unit, and characters sent from the remote unit (screen\n"
                "messages) are transmitted back to the local unit's V.24 interface.\n"
                "During a virtual terminal session, the local unit is not available any more,\n"
                "unless you close your session by typing the DISCONNECT command or by selecting\n"
                "'Exit' on the main menu screen of the session.\n"
                "R    : Remote unit selected\n"
                "1..13: Regenerator number 1 to 13 selected"
            ),
            "DISCONNECT": (
                "SYNTAX: Disconnect or DIS\n"
                "This command closes an open virtual terminal connection to the remote unit."
            ),
        }
    elif menu == "SM":
        SHORT_HELP = {
            "PSW [USER/ADMIN]":"          Set user/admin password",
            "CONNECT [n]":"               Connect to remote unit; n=R",
            "DISCONNECT":"                Disconnect virtual terminal",   
            "M":"                         Return to Main Menu, or previous level menu",
            "H [command]":"               Show help on command",
            "H":"                         Show available commands",
        }

        FULL_HELP = {
            "PSW":(
                "SYNTAX: PSW [USER/ADMIN]\n"
                "This command sets the user/admin password (4..8 characters)"
            ),
            "CONNECT": (
                "SYNTAX: CONNECT [n] or CO [n]\n"
                "This command opens a virtual terminal connection to the remote unit, i.e.\n"
                "characters received at the local unit's V.24 interface (keyboard messages) are\n"
                "send to the remote unit, and characters sent from the remote unit (screen\n"
                "messages) are transmitted back to the local unit's V.24 interface.\n"
                "During a virtual terminal session, the local unit is not available any more,\n"
                "unless you close your session by typing the DISCONNECT command or by selecting\n"
                "'Exit' on the main menu screen of the session.\n"
                "R    : Remote unit selected\n"
                "1..13: Regenerator number 1 to 13 selected"
            ),
            "DISCONNECT": (
                "SYNTAX: Disconnect or DIS\n"
                "This command closes an open virtual terminal connection to the remote unit."
            ),
            "M": (
                "SYNTAX: M\n"
                "Return to main menu, or previous level menu."
            ),
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
