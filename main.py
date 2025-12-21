from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
from models import E1, Ethernet, Nx64, xDSL
from typing import Dict, Any, List
import datetime
import time
from utils import help_func
from types import MethodType


CHAR_DELAY = 50  # скорость появления строк
CONTINUES_DELAY = 1000 # скорость появления повторяющихся сообщений
class Megatrans:
    def __init__(self) -> None:
        self.model = "MGS-3M-SRL-E1B/Eth"
        self.model_desc = "MEGATRANS-3M Subrack E1/RS232/Ethernet 120 Chm"
        self.hw = "E0"
        self.sw = "3.0.V5.L.15.6 /R3.1.1"
        self.id = ""
        self.date = datetime.date.today()
        self.boot_timestamp = time.time()

        self.time_set_timestamp = time.time()
        self.base_time = datetime.datetime.now()

        self.alarm: str = "NO"   # YES/NO
        self.status_link: str = "UP" # UP/DOWN
    
    def get_runs(self) -> str:
        time_delta = time.time() - self.boot_timestamp
        days = int(time_delta // 86400)
        hours = int(time_delta // 3600)
        minutes = int((time_delta % 3600) // 60)
        seconds = int(time_delta % 60)

        return f" {days:05d}d {hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_time(self) -> str:
        delta = time.time() - self.time_set_timestamp
        current = self.base_time + datetime.timedelta(seconds=delta)
        return current.strftime("%H:%M:%S")

class timeSlot:
    def __init__(self) -> None:
        self.avail_time = 0.0
        self.unavail_time = 0.0
        self._last_check = time.time()
        self.avail_active = False 
        self.unavail_active = False
    def start_avail(self):
        self._last_check = time.time()
        self.avail_active = True

    def start_unavail(self):
        self._last_check = time.time()
        self.unavail_active = True

    def update_avail(self):
        if self.avail_active:
            now = time.time()
            delta = now - self._last_check
            self.avail_time += delta
            self._last_check = now

    def update_unavail(self):
        if self.unavail_active:
            now = time.time()
            delta = now - self._last_check
            self.unavail_time += delta
            self._last_check = now

    def stop(self):
        self.update_avail()
        self.update_unavail()
        self.avail_active = False
        self.unavail_active = False
class G826time:
    def __init__(self) -> None:
        self.g826time = timeSlot()
        self.e_time = timeSlot()
        self.eth_time = timeSlot()

    def reset_g826(self) -> str:
        self.g826time.avail_time = 0.0
        self.g826time.unavail_time = 0.0
        self.g826time._last_check = time.time()

        self.e_time.avail_time = 0.0
        self.e_time.unavail_time = 0.0
        self.e_time._last_check = time.time()

        return "G.826 error performance parameter reset"

    def reset_netstat(self) -> str:
        self.eth_time.avail_time = 0.0
        self.eth_time.unavail_time = 0.0
        self.eth_time._last_check = time.time()

        return "Ethernet statistics reset"
        
class COM:
    def __init__(self, role: str = "SLAVE") -> None:
        self.role = role
        self.e1 = E1()
        self.nx64 = Nx64()
        self.ethernet = Ethernet()
        self.dsl = xDSL()
        self.megatrans = Megatrans()
        self.menu: str = "MM"
        self.message_prefix:str = f"{'CP' if self.role == 'SLAVE' else 'CO'}_01_1_{self.menu}>Select [1..6]: "
        self.time: str = ""
        self.timers = G826time()

        self.connected: bool = False

        self.service_interfaces = ["N"]
        self.nx64.clockmode = self.nx64._clockmode

        self.timers.g826time.start_avail()

        self.MENU_COMMANDS = {
            "MM": {
                "1": self.activate_PM,
                "2": self.activate_FMM,
                "3": self.activate_CM,
                "4": self.activate_SM,
                "6": self.exit_program
            },
            "PM": {
                "G826": self.g826, #                    
                "RESETG826": self.timers.reset_g826,#   
                "DATE": self.date_perf, #              
                "TIME": self.time_perf, #              
                "NETSTAT": self.netstat_func,#          
                "RESETNETSTAT": self.timers.reset_netstat,#
                "CONNECT": self.connect_cmd,#          
                "DISCONNECT": self.disconnect_cmd,#    
                "M": self.back_to_main,#                
            },
            "FMM": {
                "SQ": "",  #ДОДЕЛАТЬ
                "STARTUP": self.startup_func,#        
                "STATUS": self.status_func,#          
                "LOOP1": self.loop1_func, #    LOOP1 [E/N] [ON/OFF]
                "LOOP2": self.loop2_func, #            
                "RESTART": self.restart_func,#         
                "CONNECT": self.connect_cmd,#          
                "DISCONNECT": self.disconnect_cmd,#    
                "M": self.back_to_main,#               
            },
            "CM": {
                "CONFIG": self.interfaces_config,#     
                "HW": self.hw_func,#                   
                "G704": self.g704_func,#               
                "CRC4": self.crc4_func, #              
                "EBIT": self.ebit_func,#               
                "AISGEN": self.aisgen_func,#          
                "AISDET": self.aisdet_func,#          
                "EXTCLK": self.extclk_func,#            
                "PCM": self.pcm_func,#                  
                "IDLECAS": self.idlecas_func,#          
                "IDLEPAT": self.idlepat_func,#          
                "SIGSLOTS": self.sigs_func,#           
                "SERVICE": self.service,#                
                "TYPE": self.type_func,#                
                "BITRATE": self.bitrate_func,#          
                "CLOCKMODE": self.clockmode_func,#      
                "CLOCKDIR": self.clockdir_func,#        
                "SLOTUSAGE": self.slotusage_func,#      
                "MASTER": self.master_func,#            
                "PLL": self.pll_func,#                  
                "POWER": self.power_func,#              
                "RS232SLOT": self.rs232slot_func,#      
                "RS232BITS": self.rs232bits_func,#      
                "RS232RATE": self.rs232rate_func,#      
                "RS232ERATE": self.rs232erate_func,#    
                "AUTORST": self.autorst_func,#          
                "BASERATE": self.baserate_func,#        
                "ADAPT": self.adapt_func,#              
                "SCALE": self.scale_func,#              
                "DEFAULT": self.default_func,#          
                "ID": self.id_func,#                    
                "ETHSD": self.ethsd_func,#             
                "ETHPAYLOAD": self.ethpayload_func,#    
                "CONNECT": self.connect_cmd,#           
                "DISCONNECT": self.disconnect_cmd,#     
                "M": self.back_to_main#                  
            },
            "SM": {
                "PSW": "",  #ДОДЕЛАТЬ
                "M": self.back_to_main#                 
            }
        }
        for menu_name, menu_dict in self.MENU_COMMANDS.items():
            if menu_name != "MM": 
                menu_dict["H"] = MethodType(help_func, self)

    

    def loop1_func(self, *args) -> str:
        if len(args) != 2:
            return "Invalid command!\n"
        
        interface = args[0]
        value = args[1]


        if value not in ("ON", "OFF") or interface not in ("E", "N"):
            return "Illegal parameter(s)!\n"
        
        msg = f"Loop 1 on {interface} interface {value.lower()}"
        return msg

    def loop2_func(self, *args) -> str:
        if len(args) != 2:
            return "Invalid command!\n"
        
        interface = args[0]
        value = args[1]


        if value not in ("ON", "OFF") or interface not in ("L", "R"):
            return "Illegal parameter(s)!\n"
        
        msg = f"{'Local' if interface == 'L' else 'Remote'} loop {'deactivation' if value == 'OFF' else 'activation'} started\n Remote loop {'on' if value == 'ON' else 'OFF'}\n"
        
        return msg

    def restart_func(self) -> str:
        #ДОБАВИТЬ ВКЛЮЧЕНИЕ ЛАМПОЧКИ CTS(выключение DSR, RI)

        return "Restarting channel\n"

    def status_func(self) -> str:
        if self.dsl.active:
            return (
                "----------------------------------------------------------------------\n"
                "Local System Status\n"
                "----------------------------------------------------------------------\n"
                "LOSD      :     0\n"
                "SEQA      :     0\n"
                "PS        :     0\n"
                "SEGD      :     0\n"     
                "Tx power  :  13.5 dBm\n"
                "Rx gain   :  14.9 dB\n"
                "Loop attn.:  07.8 dB\n"
                f"SNR       :  {self.dsl.snr} dB\n"    
                f"Bitrate   :  {self.dsl.bitrate} kbit/s\n"
                f"Annex     :  {self.dsl.annex}\n"
                f"Power     :   {'off' if not self.dsl.active else 'Short circuit'}\n"
                "Address   :    01 (RACKADDR)\n"
                "----------------------------------------------------------------------\n"
            )
        else:
            return (
            "----------------------------------------------------------------------\n"
                "Local System Status\n"
                "----------------------------------------------------------------------\n"
                "LOSD      :     -\n"
                "SEQA      :     -\n"
                "PS        :     -\n"
                "SEGD      :     -\n"
                "Tx power  :  --.- dBm\n"
                "Rx gain   :  --.- dB\n"
                "Loop attn.:  --.- dB\n"
                f"SNR       :  --.- dB\n"    
                f"Bitrate   :  ---- kbit/s\n"
                f"Annex     :  -\n"
                f"Power     :   {'off' if not self.nx64._status else 'Short circuit'}\n"
                "Address   :    01 (RACKADDR)\n"
                "----------------------------------------------------------------------\n"
            )

    def startup_func(self) -> str:
        if self.dsl.startup == False:
            return (
                "DSL transceiver startup trace on\n"
                "No activity\n"
                "Equalizer Training\n"
                "Load cotom\n"
                "Transmit Tc\n"
                "Load codm\n"
                "No activity\n"
            )
        else:
            return (
                "DSL transceiver startup trace off\n" 
                "Remote loop off\n"
            )

    def rs232slot_func(self, *args) -> str:
        if len(args) != 1:
            return "Invalid command!\n"
    
        try:
            value = int(args[0])
        except ValueError:
            return "Invalid command!\n"
        
        if self.nx64.type != "RS232":
            return (
                "ERROR!\n"
                "Change Nx64 interface type to RS232 (TYPE 4) first!\n"
            )
        else:
            self.nx64._rs232slot = value
        
        return self.interfaces_config()

    def scale_func(self, *args):
        if len(args) != 1:
            return "Invalid command!\n"

        try:
            value = float(args[0])
        except ValueError:
            return "Invalid command!\n"

        if not -16.0 <= value <= 2.0:
            return "Illegal parameter(s)!\n"
        if (value * 2) % 1 != 0:
            return "Illegal parameter(s)!\n"

        self.dsl.scale = value
        return self.interfaces_config()

    def adapt_func(self, *args):
        if len(args) != 1:
            return "Invalid command!\n"
        mode = args[0]
        if mode not in ("OFF", "ON"):
            return "Illegal parameter(s)!\n"
        self.dsl.adapt = (mode == "ON")
        return self.interfaces_config()

    def baserate_func(self, *args):
        if len(args) != 1:
            return "Invalid command!\n"

        try:
            n = int(args[0])
        except ValueError:
            return "Invalid command!\n"

        if not 3 <= n <= 36:
            return "Illegal parameter(s)!\n"

        if self.nx64.adapt != False:
            return "BASERATE is not allowed when ADAPT is enabled\n"

        self.dsl.base_rate = n
        return self.interfaces_config()

    def autorst_func(self, *args):
        if len(args) != 1:
            return "Invalid command!\n"

        value = args[0]
        if value not in ("ON", "OFF"):
            return "Illegal parameter(s)!\n"

        self.dsl.auto_restart = (value == "ON")
        return self.interfaces_config()

    def rs232erate_func(self, *args):
        if "N" not in self.service_interfaces:
            return (
                "ERROR!\n"
                "Change service to enable Nx64 interface (SERVICE ..N..) first!\n"
            )
        if self.nx64.type != "RS232":
            return (
                "type TYPE 5 first\n"
            )

        if len(args) != 1:
            return "Invalid command!\n"

        try:
            n = int(args[0])
        except ValueError:
            return "Invalid command!\n"

        erates = {
            1: 0.0,
            2: 0.5,
            3: 1.0,
            4: 2.0
        }

        if n not in erates:
            return "Illegal parameter(s)!\n"

        self._rs232erate = erates[n]

        return self.interfaces_config()


    def rs232bits_func(self, *args):
        if "N" not in self.service_interfaces:
            return (
                "ERROR!\n"
                "Change service to enable Nx64 interface (SERVICE ..N..) first!\n"
            )
        if self.nx64.type != "RS232":
            return (
                "type TYPE 5 first\n"
            )
        
        if len(args) != 1:
            return "Invalid command!\n"

        try:
            n = int(args[0])
        except ValueError:
            return "Invalid command!\n"

        if not 7 <= n <= 10:
            return "Illegal parameter(s)!\n"

        self.nx64._rs232bits = n

        return self.interfaces_config()

    def rs232rate_func(self, *args):
        if "N" not in self.service_interfaces:
            return (
                "ERROR!\n"
                "Change service to enable Nx64 interface (SERVICE ..N..) first!\n"
            )
        if self.nx64.type != "RS232":
            return (
                "type TYPE 5 first\n"
            )

        if len(args) != 1:
            return "Invalid command!\n"

        try:
            rate = int(args[0])
        except ValueError:
            return "Invalid command!\n"

        allowed = {
            110, 150, 300, 600, 1200, 2400, 4800,
            9600, 14400, 19200, 28800, 38400,
            57600, 115200
        }

        if rate not in allowed:
            return "Illegal parameter(s)!\n"

        self.nx64._rs232rate = rate
        self.nx64._rsr232ts = 2 if rate == 115200 else 1

        return self.interfaces_config()

    def slotusage_func(self, *args):
        if len(args) != 1:
            return "Invalid command!\n"

        value = args[0]
        if value not in ("ON", "OFF"):
            return "Illegal parameter(s)!\n"

        self.nx64._slotusage = (value == "ON")
        return self.interfaces_config()


    def _default_0(self) -> str:
        self.service_interfaces = ['E']
        self.e1.g704_turn_off()
        self.e1.aisdet_turn_on()
        self.e1.aisgen_turn_on()
        self.e1.extclk_turn_off()

        self.role = "MASTER"
        self.dsl.auto_restart = True
        self.dsl.pll = False
        self.dsl.use_time_slot_0 = False

        self.nx64._type = "V.35"
        self.nx64._bitrate = 256e3
        self.nx64._clockmode = "FROM_E1"
        self.nx64._clockdir = "CONTRA"

        return self.get_main_menu_text()

    def _default_1(self) -> str:
        self.e1.g704_turn_on()
        self.e1.change_pcm(31, None)
        self.e1._idlecas = None
        self.e1._signal_slot = None

        self.role = "MASTER"

        self.nx64._type = "V.35"
        self.nx64._bitrate = 512e3
        self.nx64._clockmode = "FROM_E1"
        self.nx64._clockdir = "CONTRA"

        return self.get_main_menu_text()


    def _default_2(self) -> str:
        self.e1.g704_turn_on()
        self.e1.change_pcm(31, None)
        self.e1._signal_slot = None

        self.role = "MASTER"

        self.nx64._type = "V.35"
        self.nx64._bitrate = 1024e3
        self.nx64._clockmode = "FROM_E1"
        self.nx64._clockdir = "CONTRA"

        return self.get_main_menu_text()


    def _default_3(self) -> str:
        self.e1.g704_turn_off()
        self.e1._aisgen = True
        self.e1._aisdet = True
        
        self.role = "SLAVE"
        
        self.nx64._type = "V.35"
        self.nx64._bitrate = 256e3
        self.nx64._clockmode = "REMOTE"
        self.nx64._clockdir = "CONTRA"

        return self.get_main_menu_text()

    def _default_4(self) -> str:
        self.e1.g704_turn_on()
        self.e1.change_pcm(31, None)
        self.e1._idlecas = None
        self.e1._signal_slot = None

        self.role = "SLAVE"
        
        self.nx64._type = "V.35"
        self.nx64._bitrate = 512e3
        self.nx64._clockmode = "REMOTE"
        self.nx64._clockdir = "CONTRA"
        
        return self.get_main_menu_text()

    def _default_5(self) -> str:
        self.e1.g704_turn_on()
        self.e1.change_pcm(31, None)
        self.e1._signal_slot = None

        self.role = "SLAVE"
        
        self.nx64._type = "V.35"
        self.nx64._bitrate = 1024e3
        self.nx64._clockmode = "REMOTE"
        self.nx64._clockdir = "CONTRA"

        return self.get_main_menu_text()


    def default_func(self, *args):
        if len(args) != 1:
            return "Invalid command!\n"

        try:
            arg = int(args[0])
        except ValueError:
            return "Invalid command!\n"

        default_settings = {
            0: self._default_0,
            1: self._default_1,
            2: self._default_2,
            3: self._default_3,
            4: self._default_4,
            5: self._default_5,
        }

        if arg not in default_settings:
            return "Illegal parameter(s)!\n"

        return default_settings[arg]()

    def pll_func(self, *args):
        if len(args) == 1:
            if args[0] == "ON":
                self.dsl.pll = True
                return self.interfaces_config()
            elif args[0] == "OFF":
                self.dsl.pll = False
                return self.interfaces_config()
            else:
                return "Illegal parameter(s)!\n"
        else:
            return "Invalid command!\n"

    def connect_cmd(self, *args):
        app = self.app

        if not args or args[0] != "R":
            return "Illegal parameter(s)!\n"

        return app.connection_manager.connect_auto(self)

    def disconnect_cmd(self):
        return self.app.connection_manager.disconnect(self)



    def ethpayload_func(self, *args) -> str:
        if "ETH" not in self.service_interfaces:
            return (
                "Change service to enable Ethernet interface (SERVICE ..ETH..) first!\n"
            )
        
        if not args:
            return "Invalid command!\n"
        
        if len(args) > 1:
            return "Invalid command!\n"
        
        try:
            number = int(args[0])
            if 1 <= number <= 36:
                self.ethernet.ethpayload = number
                return self.interfaces_config()
            else:
                return "Invalid command!\n"
        except Exception:
            return "Invalid command!\n"


    def ethsd_func(self, *args) -> str:
        if "ETH" not in self.service_interfaces:
            return (
                "Change service to enable Ethernet interface (SERVICE ..ETH..) first!\n"
            )

        if not args:
            return "Invalid command!\n"

        arg0 = args[0]

        if arg0 == "AUTO":
            self.ethernet.speed = "AUTO"
            self.ethernet.duplex = "F"
            return self.interfaces_config()

        if arg0 in ("10", "100"):
            if len(args) != 2:
                return "Illegal parameter(s)!\n"
            arg1 = args[1].upper()
            if arg1 not in ("F", "H"):
                return "Illegal parameter(s)!\n"

            self.ethernet.speed = arg0
            self.ethernet.duplex = arg1
            return self.interfaces_config()

        return "Illegal parameter(s)!\n"
        

    def bitrate_func(self, *args) -> str:
        if "N" not in self.service_interfaces:
            return (
                "ERROR!\n"
                "Change service to enable Nx64 interface (SERVICE ..N..) first!\n"
            )

        if len(args) != 1:
            return "Illegal parameter(s)!\n"

        try:
            N = int(args[0])
        except ValueError:
            return "Illegal parameter(s)!\n"

        nx_type = self.nx64.type

        if nx_type == "RS232":
            return (
                "ERROR!\n"
                "Change Nx64 interface type (TYPE [0..3]) first!\n"
            )

        limits = {
            "V.28": 3,
            "V.35": 35,
            "V.36/X.21 no term.": 35,
            "V.36/X.21 with term.": 35
        }

        max_val = limits.get(nx_type, 35)

        if N < 1 or N > max_val:
            return "Illegal parameter(s)!\n"

        self.nx64._bitrate = N * 64000
        return self.interfaces_config()
        

    def sigs_func(self, *args) -> str:
        if not self.service_interfaces or "E" not in self.service_interfaces:
            return "Change service to enable E1 interface (SERVICE ..E..) first!\n"

        if self.e1.pcm[0] != 30:
            return (
                "ERROR!\n"
                "Set signalling timeslot processing enable (PCM 30) first!\n"
            )

        if len(args) == 1 and args[0] == "AUTO":
            self.e1._signal_slot = "AUTO"
            return self.interfaces_config()

        if len(args) == 1 and "," in args[0]:
            try:
                a_str, e1_str = args[0].split(",")
                a = int(a_str)
                e1 = int(e1_str)
            except ValueError:
                return "Illegal parameter(s)!\n"

            if not (1 <= a <= 31 and 1 <= e1 <= 31):
                return "Illegal parameter(s)!\n"

            self.e1._signal_slot = (a, e1)
            return self.interfaces_config()

        return "Illegal parameter(s)!\n"

    def pcm_func(self, *args) -> str:
        if not self.service_interfaces or "E" not in self.service_interfaces:
            return "Change service to enable E1 interface (SERVICE ..E..) first!\n"
        if not self.e1.g704:
            return (
                "ERROR!\n"
                "Set E1 framed mode (G704 ON) first!\n"
            )

        if len(args) == 1:
            if args[0] == "31":
                try:
                    self.e1.change_pcm(31, None)
                    return self.interfaces_config()
                except Exception:
                    return "Illegal parameter(s)!\n"
            else:
                return "Illegal parameter(s)!\n"

        if len(args) == 2:
            pcm, mode = args

            if pcm != "30":
                return "Illegal parameter(s)!\n"

            if mode not in ("C", "T"):
                return "Illegal parameter(s)!\n"

            try:
                self.e1.change_pcm(30, mode)
                return self.interfaces_config()
            except Exception:
                return "Illegal parameter(s)!\n"

        return "Invalid command!\n"

    def g704_func(self, *args) -> str:
        if not self.service_interfaces or "E" not in self.service_interfaces:
            return "Change service to enable E1 interface (SERVICE ..E..) first!\n"
        
        if len(args) == 1:
            if args[0] == "OFF":
                self.e1.g704_turn_off()
                return self.interfaces_config()
            elif args[0] == "ON":
                self.e1.g704_turn_on()
                return self.interfaces_config()
            else:
                return "Illegal parameter(s)!\n"
        return "Invalid command!\n"


    def hw_func(self) -> str:
        return (
            "----------------------------------------------------------------------\n"
            "Hardware Configuration\n"
            "----------------------------------------------------------------------\n"
            "  FPGA Type       :  CYCLONE:0\n"
            "  FPGA Rev        :  10\n"
            "  EEPROM Type     :  16K PB1: 5C07 PB2: 5C07\n"
            "  FRAMER E1       :  Ch A - DS2155 Rev.04; Ch B - DS2155 Rev.04;\n"
            "  DSP/FRAMER DSL  :  GS2237 Rev.00, Ver.  R3.1.1\n"
            "  SVN             :  1096\n"
            "  Ethernet chip   :  ADM6993 Rev.0002114.2\n"
            "  Serial number   :  17N18764\n"
            "----------------------------------------------------------------------"
        )

    def netstat_func(self) -> str:
        if not self.service_interfaces or "ETH" not in self.service_interfaces:
            return "Change service to enable Ethernet interface (SERVICE ..ETH..) first!"
        self.timers.eth_time.update_avail()
        self.timers.eth_time.update_unavail()
        return (
            "----------------------------------------------------------------------\n"
            "Statistics           Ethernet connection\n"
            "----------------------------------------------------------------------\n"
            "Bytes transmitted    : 0000000000\n"
            "Packets transmitted  : 0000000000\n"
            "Bytes received       : 0000000000\n"
            "Packets received     : 0000000000\n"
            "Errors               : 0000000000\n"
            "Collision            : 0000000000\n"
            f"Available time       : {int(self.timers.eth_time.avail_time):010d}\n"
            f"Unavailable time     : {int(self.timers.eth_time.unavail_time):010d}\n"
            "----------------------------------------------------------------------"
        )
    
    def idlecas_func(self, *args) -> str:
        if len(args) != 1:
            return "Invalid command!\n"
        if not self.service_interfaces or "E" not in self.service_interfaces:
            return "Change service to enable E1 interface (SERVICE ..E..) first!"
        if  self.e1.pcm[0] == 31:
            return (
                "ERROR!\n"
                "Set signalling timeslot processing enable (PCM 30) first!\n"
            )
        try:
            self.e1.set_idlecas(args[0])
            return self.interfaces_config()
        except Exception:
            return "Illegal parameter(s)!\n"
        

    def idlepat_func(self, *args) -> str:
        if len(args) != 1:
            return "Invalid command!\n"
        if not self.service_interfaces or "E" not in self.service_interfaces:
            return "Change service to enable E1 interface (SERVICE ..E..) first!"
        if not self.e1.g704:
            return (
                "ERROR!\n"
                "Set E1 framed mode (G704 ON) first!\n"
            )
        try:
            self.e1.set_idlepat(args[0])
            return self.interfaces_config()
        except Exception:
            return "Illegal parameter(s)!\n"
    
    def id_func(self, *args) -> str:
        if not args:
            return f"{self.megatrans.id}"
        if len(args) == 1:
            arg = args[0]
            if len(arg) > 20:
                return "Illegal parameter(s)!\n"
            self.megatrans.id = arg
            return None
        return "Invalid command!\n"

    def type_func(self, *args) -> str:
        if len(args) != 1:
            return "Invalid command!\n"

        arg = args[0]

        if arg not in self.nx64.INTERFACES:
            return "Illegal parameter(s)!\n"

        if not self.service_interfaces or "N" not in self.service_interfaces:
            return "Change service to enable Nx64 interface (SERVICE ..N..) first!\n"

        self.nx64.set_type(arg)

        return self.interfaces_config()

    def clockdir_func(self, *args) -> str:
        if len(args) != 1:
            return "Invalid command!\n"
        arg = args[0]
        if not  self.service_interfaces or "N" not in self.service_interfaces:
            return "Change service to enable Nx64 interface (SERVICE ..N..) first!\n"
        
        if self.nx64.clockmode != "INT" and arg == "CONTRA":
            return (
                "ERROR!\n"
                "Change clock mode to internal (CLOCKMODE INT) first!"
            )
        if arg not in ("CO", "CONTRA"):
            return "Illegal parameter(s)!\n"
    
        try:
            self.nx64.set_clockdir(arg)
            return self.interfaces_config()
        except ValueError:
            return "Invalid command!\n"



    def clockmode_func(self, *args) -> str:
        if len(args) != 1:
            return "Invalid command!\n"

        arg = args[0]

        if not self.service_interfaces or "N" not in self.service_interfaces:
            return "Change service to enable Nx64 interface (SERVICE ..N..) first!\n"

        if "E" in self.service_interfaces and "N" in self.service_interfaces:
            self.nx64.clockmode = "FROM_E1"
            return self.interfaces_config()

        if arg not in ("EXT", "INT"):
            return "Illegal parameter(s)!\n"

        try:
            self.nx64.set_clockmode(arg, self.role)
            return self.interfaces_config()
        except ValueError:
            return "Invalid command!\n"

    def master_func(self, *args) -> str:
        if len(args) == 1:
            arg = args[0]
            if arg == "ON":
                if self.role == "SLAVE":
                    self.role = "MASTER"
                    self.update_message_prefix()
                    #СДЕЛАТЬ ВКЛЮЧЕНИЕ ЗВУКА ПЕРЕКЛЮЧЕНИЯ КНОПКИ А ТАКЖЕ ДОБАВИТЬ ЛОГИКУ РАБОТЫ С СВЕТОДИОДАМИ(зелёный-оранджевый и ТД)
                return None
            elif arg == "OFF":
                if self.role == "MASTER":
                    self.role = "SLAVE"

                    # корректно через метод
                    try:
                        self.nx64.set_clockdir("REMOTE")
                    except Exception:
                        pass  # если нельзя — просто игнорируем

                    self.update_message_prefix()
                return None
            else:
                return "Illegal parameter(s)!\n"
        return "Invalid command!\n"
        

    def power_func(self, *args) -> str:
        if len(args) == 1:
            arg = args[0]
            if arg == "ON":
                self.nx64.power_on()
                self.ethernet.power_on()
                self.dsl.active = True
                return self.interfaces_config()
            elif arg == "OFF":
                self.nx64.power_off()
                self.ethernet.power_off()
                self.dsl.active = False
                return self.interfaces_config()
            else:
                return "Illegal parameter(s)!\n"
        return "Invalid command!\n"

    def extclk_func(self, *args) -> str:
        if not self.service_interfaces or "E" not in self.service_interfaces:
            return "Change service to enable E1 interface (SERVICE ..E..) first!"
        if len(args) == 1:
            arg = args[0]
            if arg == "ON":
                self.e1.extclk_turn_on()
                return self.interfaces_config()
            elif arg == "OFF":
                self.e1.extclk_turn_off()
                return self.interfaces_config()
            else:
                return "Illegal parameter(s)!\n"
        return "Invalid command!\n"

    def aisgen_func(self, *args) -> str:
        if not self.service_interfaces or "E" not in self.service_interfaces:
            return "Change service to enable E1 interface (SERVICE ..E..) first!"
        if len(args) == 1:
            arg = args[0]
            if arg == "ON":
                self.e1.aisgen_turn_on()
                return self.interfaces_config()
            elif arg == "OFF":
                self.e1.aisgen_turn_off()
                return self.interfaces_config()
            else:
                return "Illegal parameter(s)!\n"
        return "Invalid command!\n"


    def aisdet_func(self, *args) -> str:
        if not self.service_interfaces or "E" not in self.service_interfaces:
            return "Change service to enable E1 interface (SERVICE ..E..) first!"
        if len(args) == 1:
            arg = args[0]
            if arg == "ON":
                self.e1.aisdet_turn_on()
                return self.interfaces_config()
            elif arg == "OFF":
                self.e1.aisdet_turn_off()
                return self.interfaces_config()
            else:
                return "Illegal parameter(s)!\n"
        return "Invalid command!\n"

    def ebit_func(self, *args) -> str:
        if not self.e1.g704:
                return (
                    "ERROR!\n"
                    "Set E1 framed mode (G704 ON) first!\n"
                )
        if not self.e1.crc4:
            return(
                "ERROR!\n"
                "Turn on CRC4 mode (CRC4 ON) first!\n"
            )
        if len(args) == 1:
            arg = args[0]
            if arg == "ON":
                self.e1.ebit_turn_on()
                return self.interfaces_config()
            elif arg == "OFF":
                self.e1.ebit_turn_off()
                return self.interfaces_config()
            else:
                return "Illegal parameter(s)!\n"
        return "Invalid command!\n"


    def crc4_func(self, *args) -> str:
        if len(args) == 1:
            if not self.e1.g704:
                return (
                    "ERROR!\n"
                    "Set E1 framed mode (G704 ON) first!\n"
                )
            arg = args[0]
            if arg == "ON":
                self.e1.crc4_turn_on()
                return self.interfaces_config()
            elif arg == "OFF":
                self.e1.crc4_turn_off()
                return self.interfaces_config()
            else:
                return "Illegal parameter(s)!\n"
        return "Invalid command!\n"
    
    def get_e1_info(self) -> str:
        if self.e1.g704:
            pcm_type, has_sig, sig_mode = self.e1.pcm

            if pcm_type == 31:
                pcm_info = "PCM31"
                sig_info = ""
            else:
                pcm_info = "PCM30"
                sig_info = "CAS" if sig_mode == "C" else "Transparent"

            slot = self.e1.signal_slot
            if slot is None:
                sig_ts = "--"
            elif slot == "AUTO":
                sig_ts = "AUTO"
            else:
                a, e1 = slot
                sig_ts = f"A={a:02d},E1={e1:02d}"

            msg = (
                "G.703 interface, Framing : ITU-T G.704\n"
                f" PCM Mode : {pcm_info}, {sig_info}\n"
                f" Idle CAS : {'--' if self.e1.idlecas is None else f'0x{self.e1.idlecas:X}'}\n"
                f" Signalling TS : {sig_ts}\n"
            )
        else:
            msg = (
                "G.703 interface, Framing : Transparent\n"
                f" AIS Det/Gen : {'on' if self.e1.aisdet else '--'}/"
                f"{'on' if self.e1.aisgen else '--'}\n"
                f" External Clock : {'on' if self.e1.extclk else '--'}\n"
            )

        return msg
    
    def get_nx_info(self) -> str:
        mode = "from E1" if self.nx64.clockmode == "FROM_E1" else self.nx64.clockmode
        return (
            f"Nx64 interface,    Interface Type :  {self.nx64.type}\n"
            f"      Clock Mode       :  {mode}\n"
            f"      Clock Direction  :  "
            f"{'codirectional' if self.nx64.clockdir == 'CO' else 'contradirectional'}\n"
        )
    
    def get_eth_info(self) -> str:
        msg = (
            "Ethernet interface\n"
            f"      Eth Payload      :  30 TS\n"
        )
        return msg
    
    def get_xdsl_info(self) -> str:
        msg = (
            f"xDSL interface,    Master/Slave :  {'Slave' if self.role == 'SLAVE' else 'Master'}\n"
            f"       Autorestart     :  {'on' if True else '--'}\n"       #ПРОВЕРИТЬ
            f"       PLL             :  {'on' if self.dsl.pll else 'off'}\n"
            f"       Use Timeslot 0  :  {'--db' if True else '--'}\n"      #ПРОВЕРИТЬ
            f"       Idle Pattern    :  {hex(self.e1.idlepat).upper()}\n"
            "----------------------------------------------------------------------"
        )
        return msg


    def interfaces_config(self) -> str:
        if not self.service_interfaces:
            return None
        handlers = {"E": self.get_e1_info, "N": self.get_nx_info, "ETH": self.get_eth_info}
        
        preview = (
            "----------------------------------------------------------------------\n"
            f"       Service         :  {','.join(self.service_interfaces)}\n"
            "----------------------------------------------------------------------\n"
        )
        output = []
        output.append(preview)

        for interface  in self.service_interfaces:
            func = handlers.get(interface)
            if func:
                output.append(func())
        output.append(self.get_xdsl_info())
        return "".join(output)

    def service(self, *args) -> str:
        if not args:
            return "Invalid command!\n"

        try:
            arg = args[0]
            parts = [p for p in arg.split(",")]

            interfaces = {"E", "N", "ETH"}

            if not (1 <= len(parts) <= 3):
                return "Illegal parameter(s)!"
            if not set(parts).issubset(interfaces):
                return "Illegal parameter(s)!"
            if len(parts) != len(set(parts)):
                return "Illegal parameter(s)!"

            new_service = parts
            old_service = self.service_interfaces or []

            self.service_interfaces = new_service

            # Включили E при активном N
            if "N" in new_service and "E" in new_service and "E" not in old_service:
                # сохраняем ТОЛЬКО пользовательский режим
                if self.nx64.clockmode != "FROM_E1":
                    self.nx64.saved_clockmode = self.nx64.clockmode
                self.nx64.clockmode = "FROM_E1"

            # Выключили E, но N остался
            elif "N" in new_service and "E" not in new_service and "E" in old_service:
                self.nx64.clockmode = self.nx64.saved_clockmode

            if "E" in new_service and "E" not in old_service:
                self.timers.e_time.start_unavail()
            elif "E" not in new_service and "E" in old_service:
                self.timers.e_time.stop()

            if "ETH" in new_service and "ETH" not in old_service:
                self.timers.eth_time.start_unavail()
            elif "ETH" not in new_service and "ETH" in old_service:
                self.timers.eth_time.stop()

            return self.interfaces_config()

        except Exception:
            return "Illegal parameter(s)!"


    def date_perf(self, *args) -> str:
        if not args:
            return f"Current date: {self.megatrans.date.strftime('%d/%m/%Y')}"

        try:
            d, m, y = map(int, args[0].split("/"))
            self.megatrans.date = datetime.date(y, m, d)
            return None
        except Exception:
            return "Illegal parameter(s)!"


    def time_perf(self, *args) -> str:
        if not args:
            return f"Current time: {self.megatrans.get_time()}"

        try:
            h, m, s = map(int, args[0].split(":"))

            self.megatrans.base_time = datetime.datetime.now().replace(
                hour=h, minute=m, second=s
            )
            self.megatrans.time_set_timestamp = time.time()

            return None
        except Exception:
            return "Illegal parameter(s)!"

    def g826(self, *args) -> str:
        if self.e1.crc4:
            Err_perf_message = "CRC4      E-Bit"
        else:
            Err_perf_message = "FAS"

        

        if not args:
            self.timers.g826time.update_avail()
            self.timers.g826time.update_unavail()
            msg = (
                "----------------------------------------------------------------------\n"
                "G.826 Error Performance   :    CRC6\n"
                "----------------------------------------------------------------------\n"
                "Errored blocks           :  0000000000\n"
                "Severely errored seconds :  0000000000\n"
                "Background block errors  :  0000000000\n"
                f"Available time           :  {int(self.timers.g826time.avail_time):010d}\n"
                f"Unavailable time         :  {int(self.timers.g826time.unavail_time):010d}\n"
                "----------------------------------------------------------------------"
            )
            return msg
        elif args == ("E1",):
            self.timers.e_time.update_avail()
            self.timers.e_time.update_unavail()
            if not self.service_interfaces or "E" not in self.service_interfaces:
                return "Change service to enable E1 interface (SERVICE ..E..) first!"
            msg = (
                "----------------------------------------------------------------------\n"
                f"G.826 Error Performance   :    {Err_perf_message}\n"
                "----------------------------------------------------------------------\n"
                f"Errored blocks           :  0000000000\n"
                f"Severely errored seconds :  0000000000\n"
                f"Background block errors  :  0000000000\n"
                f"Available time           :  {int(self.timers.e_time.avail_time):010d}\n"
                f"Unavailable time         :  {int(self.timers.e_time.unavail_time):010d}\n"
                "----------------------------------------------------------------------"
            )
            return msg
        elif args == ("C",):
            self.timers.g826time.update_avail()
            self.timers.g826time.update_unavail()
            msg = (
                "__CONTINUE__"
                "----------------------------------------------------------------------\n"
                "G.826 Error Performance   :    CRC6\n"
                "----------------------------------------------------------------------\n"
                "Errored blocks           :  0000000000\n"
                "Severely errored seconds :  0000000000\n"
                "Background block errors  :  0000000000\n"
                f"Available time           :  {int(self.timers.g826time.avail_time):010d}\n"
                f"Unavailable time         :  {int(self.timers.g826time.unavail_time):010d}\n"
                "----------------------------------------------------------------------\n"
                f"{self.message_prefix}"
            )
            return msg
        elif args == ("E1", "C"):
            if not self.service_interfaces or "E" not in self.service_interfaces:
                return "Change service to enable E1 interface (SERVICE ..E..) first!"
            self.timers.e_time.update_avail()
            self.timers.e_time.update_unavail()
            msg = (
                "__CONTINUE__"
                "----------------------------------------------------------------------\n"
                f"G.826 Error Performance   :    {Err_perf_message}\n"
                "----------------------------------------------------------------------\n"
                f"Errored blocks           :  0000000000\n"
                f"Severely errored seconds :  0000000000\n"
                f"Background block errors  :  0000000000\n"
                f"Available time           :  {int(self.timers.e_time.avail_time):010d}\n"
                f"Unavailable time         :  {int(self.timers.e_time.unavail_time):010d}\n"
                "----------------------------------------------------------------------\n"
                f"{self.message_prefix}"
            )
            return msg
        else:
            return "Illegal parameter(s)!\n"

    def activate_PM(self) -> str:
        self.menu = "PM"
        self.update_message_prefix()
        return "Performance management activated\nEnter <M> to return to MAIN, or <H> for HELP information"

    def activate_FMM(self) -> str:
        self.menu = "FMM"
        self.update_message_prefix()
        return "Fault and maintenance management activated\nEnter <M> to return to MAIN, or <H> for HELP information"

    def activate_CM(self) -> str:
        self.menu = "CM"
        self.update_message_prefix()
        return "Configuration management activated\nEnter <M> to return to MAIN, or <H> for HELP information"

    def activate_SM(self) -> str:
        self.menu = "SM"
        self.update_message_prefix()
        return "Security management activated\nEnter <M> to return to MAIN, or <H> for HELP information"

    def exit_program(self) -> str:
        self.update_message_prefix()
        return "Exiting..."

    #back to MM
    def back_to_main(self) -> str:
        self.menu = "MM"
        self.update_message_prefix()
        return self.get_main_menu_text()

    def execute(self, cmd: str) -> str:
        if not cmd:
            return ""
        parts = cmd.strip().upper().split()
        cmd = parts[0]
        args = parts[1:]

        real_com = self.app.connection_manager.resolve_target(self)
        command_list = real_com.MENU_COMMANDS[real_com.menu] 
        if cmd in command_list:
            return command_list[cmd](*args)
        return "Invalid command!"

    def get_main_menu_text(self) -> str:
        self.menu = "MM"
        self.update_message_prefix()
        return (
            f"MODEL {self.megatrans.model}\n"
            f"HW {self.megatrans.hw}\n"
            f"SW {self.megatrans.sw}\n"
            f"DATE {self.megatrans.date.strftime('%b %d %Y')}\n"
            f"ID {self.megatrans.id}\n"
            f"RUNS{self.megatrans.get_runs()}\n"
            f"ALARM {self.megatrans.alarm}\n"
            f"STATUS LINK {self.megatrans.status_link}\n"
            f"MODEL_DESC {self.megatrans.model_desc}\n\n"
            "Copyright (C) 2006 by Nateks Ltd.\n\n"
            "------------- Main Menu -----------------\n"
            "1.  Performance management  (PM)\n"
            "2.  Fault and maintenance management (FMM)\n"
            "3.  Configuration management  (CM)\n"
            "4.  Security management  (SM)\n"
            "\n6.  Exit\n"
            "----------------------------------------\n\n"
        )
    
    def update_message_prefix(self) -> None:
        role = "CP" if self.role == "SLAVE" else "CO"

        if self.menu == "MM":
            self.message_prefix = f"{role}_01_1_{self.menu}>Select [1..6] : "
        else:
            self.message_prefix = f"{role}_01_1_{self.menu}:"
    


# -------------------------------
# Терминал
# -------------------------------
class Terminal(tk.Toplevel):
    def __init__(self, master, com: COM, settings):
        super().__init__(master)
        self.com = com
        self.settings: Dict[str, Any] = settings
        
        self.input_start: str = "1.0"
        self.locked: bool = True
        self.sequence_index = 0
        self.sequence: List["str"] = ["%", "0", "1"]

        self.output_in_progress: bool = False
        self.continue_mode: bool = False
        self.continue_text = ""

        self.port_name = self.settings.get("port")
        self.baud_rate = self.settings.get("baud_rate")
        self.data_bits = self.settings.get("data_bits")
        self.parity = self.settings.get("parity")
        self.stop_bits = self.settings.get("stop_bits")


        self.title(("{},{},{},{},{}").format(
            self.port_name,
            self.baud_rate,
            self.data_bits,
            self.parity,
            self.stop_bits
        ))

        self.geometry("600x400")
        self.attributes("-topmost", True)

        self.text = tk.Text(self, bg="black", fg="lime", insertbackground="lime")
        self.text.pack(fill="both", expand=True)

        self.text.bind("<Key>", self.on_key)
        self.text.bind("<BackSpace>", self.backspace)
        self.text.bind("<Return>", self.enter)

        for key in ["<Up>", "<Down>", "<Left>", "<Right>", "<Home>", "<End>", "<Prior>", "<Next>"]:
            self.text.bind(key, lambda e: "break")
        self.text.bind("<Button-1>", lambda e: self.text.mark_set("insert", "end"))
        self.text.bind("<Button-2>", lambda e: "break")
        self.text.bind("<Button-3>", lambda e: "break")

        self.text.mark_set("insert", "end")
        self.text.see("end")
        self.blink_cursor()



    def type_lines(self, text, index=0, done_callback=None):
        if index == 0:
            self.output_in_progress = True
            self._lines = text.splitlines(keepends=True)

        if index < len(self._lines):
            self.text.insert("end", self._lines[index])
            self.text.see("end")
            self.after(
                CHAR_DELAY,
                lambda: self.type_lines(text, index + 1, done_callback)
            )
        else:
            self.output_in_progress = False
            if done_callback:
                done_callback()

    def blink_cursor(self):
        self.text.mark_set("insert", "end")
        self.after(500, self.blink_cursor)

    def put_message_prefix(self):
        self.text.insert("end", f"{self.com.message_prefix}")
        self.text.see("end")
        self.input_start = self.text.index("end-1c")
        self.text.mark_set("insert", "end-1c")

    def get_input(self):
        return self.text.get(self.input_start, "end-1c")

    def on_key(self, event):
        if self.com.connected:
            return "break"

        if self.continue_mode:
            self.continue_mode = False
        if hasattr(self, "repeat_id") and self.repeat_id:
            self.after_cancel(self.repeat_id)
            self.repeat_id = None
            self.put_message_prefix()
            return "break"

        self.text.mark_set("insert", "end")
        self.text.see("end")

        if self.locked:
            char = event.char.upper()
            if not char or char.isspace():
                return "break"
            if char == self.sequence[self.sequence_index]:
                self.sequence_index += 1
                if self.sequence_index == len(self.sequence):
                    self.locked = False
                    self.type_lines(self.com.get_main_menu_text(), done_callback=self.put_message_prefix)
                return "break"
            else:
                self.sequence_index = 0
                return "break"

        char = event.char
        if char and char.isprintable():
            self.text.insert("end", char.upper())
            self.text.see("end")
        return "break"
    
    def backspace(self, event):
        if self.locked or self.com.connected:
            return "break"
        cur_index = self.text.index("insert")
        if self.text.compare(cur_index, ">", self.input_start):
            self.text.delete("%s-1c" % cur_index)
        return "break"
    
    def wait_for_key_to_continue(self):
        self.continue_mode = True

    def repeat_output(self):
        if not self.continue_mode:
            return

        updated_resp = self.com.execute(self.continue_text_command)

        if updated_resp.startswith("__CONTINUE__"):
            updated_resp = updated_resp.replace("__CONTINUE__", "").strip()

        self.type_lines("\n" + updated_resp + "\n")

        self.repeat_id = self.after(CONTINUES_DELAY, self.repeat_output)

    def enter(self, event):
        if self.com.connected and self.com.role == "SLAVE":    
            return "break"
        
        if self.output_in_progress:
            return "break"

        cmd = self.get_input().strip()

        if self.locked:
            return "break"

        self.text.insert("end", "\n")

        if self.com.menu == "MM":

            if not cmd:
                self.type_lines(
                    self.com.get_main_menu_text(),
                    done_callback=self.put_message_prefix
                )
                return "break"

            resp = self.com.execute(cmd)

            if resp and resp != "Invalid command!":
                self.type_lines(
                    resp + "\n",
                    done_callback=self.put_message_prefix
                )
                return "break"

            self.type_lines(
                self.com.get_main_menu_text(),
                done_callback=self.put_message_prefix
            )
            return "break"

        if not cmd:
            self.type_lines(
                "Invalid command!\n",
                done_callback=self.put_message_prefix
            )
            return "break"

        resp = self.com.execute(cmd)

        if resp is None:
            self.put_message_prefix()
            return "break"

        if resp.startswith("__CONTINUE__"):
            self.continue_text_command = cmd
            self.wait_for_key_to_continue()
            self.continue_text = resp.replace("__CONTINUE__", "").strip()
            self.repeat_output()
            return "break"

        self.type_lines(
            resp + "\n",
            done_callback=self.put_message_prefix
        )
        return "break"

class ConnectionManager:
    def __init__(self) -> None:
        self.master: COM | None = None
        self.slave: COM | None = None

    def connect_auto(self, requester: COM):
        # 1. Команда только от MASTER
        if requester.role != "MASTER":
            return "Unable to connect!\n"

        # 2. Уже есть соединение
        if self.master or self.slave:
            return ""

        for com in requester.app.com_ports.values():
            if com is requester:
                continue
            if com.role == "SLAVE" and not com.connected:
                self.master = requester
                self.slave = com
                com.connected = True
                return com.get_main_menu_text()

        return "Unable to connect!\n"

    def disconnect(self, caller: COM):
        if not self.master or not self.slave:
            return None 

        was_master = caller is self.master

        self.slave.connected = False
        self.master = None
        self.slave = None

        if was_master:
            return caller.get_main_menu_text()
        return None

    def resolve_target(self, requester: COM) -> COM:
        if requester is self.master and self.slave:
            return self.slave
        return requester
    
# -------------------------------
# Windows XP GUI main app
# -------------------------------
class WindowsXPApp:
    def __init__(self):
        self.COLORS = {
            "window_bg": "#a0a0a0",
            "menu_bg": "#ffffff",
            "dialog_bg": "#ece9d8",
            "button_bg": "#d4d0c8",
            "button_fg": "#000000",
            "border_dark": "#808080",
            "tab_bg": "#d4d0c8",
            "tab_active_bg": "#ece9d8",
            "label_fg": "#000000",
            "check_bg": "#ece9d8",
            "radio_bg": "#ece9d8",
            "listbox_bg": "#ffffff",
            "listbox_fg": "#000000",
        }

        self.FONTS = {
            "title": ("MS Sans Serif", 8, "bold"),
            "label": ("MS Sans Serif", 8),
            "button": ("MS Sans Serif", 8),
            "tab": ("MS Sans Serif", 8),
        }

        self.root = Tk()
        self.root.title("Windows XP Application")
        self.root.geometry("1024x768")
        self.root.configure(bg=self.COLORS["window_bg"])

        self.com_ports = {}
        self.terminals = {}
        self.child_windows = []

        self.create_classic_menu()
        self.create_toolbar()
        self.create_main_workspace()

        self.connection_manager = ConnectionManager()

    def create_classic_menu(self):
        menubar = Menu(self.root, bg=self.COLORS["menu_bg"], fg="black")
        self.root.config(menu=menubar)
        profile_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        profile_menu.add_command(label="New Profile")
        profile_menu.add_command(label="Open Profile...")
        profile_menu.add_command(label="Save Profile")
        profile_menu.add_separator()
        profile_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Profile", menu=profile_menu)

        edit_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        port_menu = Menu(menubar, tearoff=0, bg=self.COLORS["menu_bg"], fg="black")
        port_menu.add_command(label="Open", command=self.show_property_dialog)
        menubar.add_cascade(label="Port Manager", menu=port_menu)

    def create_toolbar(self):
        toolbar = Frame(self.root, bg=self.COLORS["window_bg"], height=32)
        toolbar.pack(fill=X, side=TOP, padx=0, pady=0)
        buttons_frame = Frame(toolbar, bg=self.COLORS["window_bg"], height=30)
        buttons_frame.pack(fill=X, side=TOP, padx=2, pady=2)

        Button(buttons_frame, text="Settings", bg=self.COLORS["button_bg"], fg=self.COLORS["button_fg"],
               font=self.FONTS["button"], relief=RAISED, command=self.show_property_dialog).pack(side=LEFT, padx=2)
        Button(buttons_frame, text="Save", bg=self.COLORS["button_bg"], fg=self.COLORS["button_fg"],
               font=self.FONTS["button"], relief=RAISED).pack(side=LEFT, padx=2)
        Button(buttons_frame, text="Exit", bg=self.COLORS["button_bg"], fg=self.COLORS["button_fg"],
               font=self.FONTS["button"], relief=RAISED, command=self.root.destroy).pack(side=LEFT, padx=2)

    def create_main_workspace(self):
        workspace = Frame(self.root, bg=self.COLORS["window_bg"])
        workspace.pack(fill=BOTH, expand=True, padx=8, pady=8)

    def show_property_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Open COM Port")
        dialog.geometry("600x400")
        dialog.configure(bg=self.COLORS["dialog_bg"])
        self.child_windows.append(dialog)

        outer_frame = Frame(dialog, bg=self.COLORS["border_dark"], borderwidth=1, relief=SOLID)
        outer_frame.pack(fill=BOTH, expand=True, padx=1, pady=1)
        main_frame = Frame(outer_frame, bg=self.COLORS["dialog_bg"])
        main_frame.pack(fill=BOTH, expand=True, padx=1, pady=1)

        # ------------------------
        # Левый блок - COM порты
        left_frame = Frame(main_frame, bg=self.COLORS["dialog_bg"])
        left_frame.pack(side=LEFT, fill=Y, padx=(10, 20), pady=10)

        Label(left_frame, text="Port:", bg=self.COLORS["dialog_bg"],
              fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(anchor=W, pady=5)
        self.port_listbox = Listbox(left_frame, bg=self.COLORS["listbox_bg"],
                                    fg=self.COLORS["listbox_fg"], height=6, selectbackground="#000080",
                                    selectforeground="#ffffff")
        self.port_listbox.pack(fill=BOTH, expand=True)

        for port_name in ["COM1", "COM2"]:
            display_name = port_name + (" *" if port_name in self.terminals else "")
            self.port_listbox.insert(END, display_name)
        self.port_listbox.selection_set(0)

        # ------------------------
        # Правый блок - параметры COM
        # ------------------------
        right_frame = Frame(main_frame, bg=self.COLORS["dialog_bg"])
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Baud rate
        baud_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        baud_frame.pack(fill=X, pady=(0,5))
        Label(baud_frame, text="Baud Rate:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        self.baud_var = StringVar(value="9600")
        ttk.Combobox(baud_frame, textvariable=self.baud_var,
                     values=["9600","19200","38400","57600","115200"],
                     state="readonly", width=15).pack(side=LEFT)
        self.user_defined_var = BooleanVar(value=False)
        Checkbutton(baud_frame, text="User defined", variable=self.user_defined_var,
                    bg=self.COLORS["check_bg"], fg=self.COLORS["label_fg"],
                    font=self.FONTS["label"]).pack(side=LEFT)

        # Data bits
        data_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        data_frame.pack(fill=X, pady=(0,5))
        Label(data_frame, text="Data bits:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        self.data_var = StringVar(value="8")
        ttk.Combobox(data_frame, textvariable=self.data_var, values=["5","6","7","8"],
                     state="readonly", width=15).pack(side=LEFT)

        # Parity
        parity_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        parity_frame.pack(fill=X, pady=(0,5))
        Label(parity_frame, text="Parity:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        self.parity_var = StringVar(value="None")
        ttk.Combobox(parity_frame, textvariable=self.parity_var,
                     values=["None","Even","Odd","Mark","Space"],
                     state="readonly", width=15).pack(side=LEFT)

        # Stop bits
        stop_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        stop_frame.pack(fill=X, pady=(0,5))
        Label(stop_frame, text="Stop bits:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        self.stop_var = StringVar(value="1")
        ttk.Combobox(stop_frame, textvariable=self.stop_var, values=["1","1.5","2"],
                     state="readonly", width=15).pack(side=LEFT)

        # Flow control
        flow_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        flow_frame.pack(fill=X, pady=(0,5))
        Label(flow_frame, text="Flow control:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        flow_control_frame = Frame(flow_frame, bg=self.COLORS["dialog_bg"])
        flow_control_frame.pack(side=LEFT)
        self.flow_var = StringVar(value="RTS/CTS")
        for val in ["RTS/CTS","DTR/DSR","XON/XOFF"]:
            Radiobutton(flow_control_frame, text=val, variable=self.flow_var, value=val,
                        bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(anchor=W)

        # RTS/DTR
        state_frame = Frame(right_frame, bg=self.COLORS["dialog_bg"])
        state_frame.pack(fill=X, pady=(5,0))

        # RTS
        rts_frame = Frame(state_frame, bg=self.COLORS["dialog_bg"])
        rts_frame.pack(fill=X, pady=(0,5))
        Label(rts_frame, text="RTS state:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        rts_state_frame = Frame(rts_frame, bg=self.COLORS["dialog_bg"])
        rts_state_frame.pack(side=LEFT)
        self.rts_var = StringVar(value="ON")
        Radiobutton(rts_state_frame, text="ON", variable=self.rts_var, value="ON",
                    bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(side=LEFT, padx=(0,10))
        Radiobutton(rts_state_frame, text="OFF", variable=self.rts_var, value="OFF",
                    bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(side=LEFT)

        # DTR
        dtr_frame = Frame(state_frame, bg=self.COLORS["dialog_bg"])
        dtr_frame.pack(fill=X)
        Label(dtr_frame, text="DTR state:", bg=self.COLORS["dialog_bg"], fg=self.COLORS["label_fg"],
              font=self.FONTS["label"], width=15, anchor=W).pack(side=LEFT)
        dtr_state_frame = Frame(dtr_frame, bg=self.COLORS["dialog_bg"])
        dtr_state_frame.pack(side=LEFT)
        self.dtr_var = StringVar(value="ON")
        Radiobutton(dtr_state_frame, text="ON", variable=self.dtr_var, value="ON",
                    bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(side=LEFT, padx=(0,10))
        Radiobutton(dtr_state_frame, text="OFF", variable=self.dtr_var, value="OFF",
                    bg=self.COLORS["radio_bg"], fg=self.COLORS["label_fg"], font=self.FONTS["label"]).pack(side=LEFT)

        # ------------------------
        # Кнопки диалога
        # ------------------------
        button_frame = Frame(main_frame, bg=self.COLORS["dialog_bg"])
        button_frame.pack(fill=X, pady=10)
        Frame(button_frame, bg=self.COLORS["dialog_bg"]).pack(side=LEFT, expand=True)

        self.ok_button = Button(button_frame, text="OK", width=10,
                                command=lambda: self.open_terminal(dialog))
        self.ok_button.pack(side=LEFT, padx=5)
        Button(button_frame, text="Cancel", width=10, command=dialog.destroy).pack(side=LEFT, padx=5)

        # ------------------------
        # Логика блокировки кнопки OK
        # ------------------------
        def update_ok_button(event=None):
            sel = self.port_listbox.curselection()
            if not sel:
                self.ok_button.config(state=DISABLED)
                return
            display_name = self.port_listbox.get(sel[0])
            if "*" in display_name:
                self.ok_button.config(state=DISABLED)
            else:
                self.ok_button.config(state=NORMAL)

        self.port_listbox.bind("<<ListboxSelect>>", update_ok_button)
        update_ok_button()

    def open_terminal(self, dialog):
        selection = self.port_listbox.curselection()
        if not selection:
            return
        port = self.port_listbox.get(selection[0]).replace(" *","")

        if port not in self.com_ports:
            com = COM(role="SLAVE")
            com.app = self
            self.com_ports[port] = com

        com_obj = self.com_ports[port]

        settings = {
        "port": port,
        "baud_rate": self.baud_var.get(),
        "data_bits": self.data_var.get(),
        "parity": self.parity_var.get(),
        "stop_bits": self.stop_var.get()
    }

        term = Terminal(self.root, com=com_obj, settings=settings,)
        self.terminals[port] = term

        def on_close():
            try:
                del self.terminals[port]
            except Exception:
                pass
            term.destroy()

        term.protocol("WM_DELETE_WINDOW", on_close)
        dialog.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = WindowsXPApp()
    app.run()
