from typing import Dict 

class Nx64:
    
    INTERFACES = ("V35", "V36_X21_WITHOUT_TERMINATION", "V36_X21_WITH_TERMINATION", "V28", "RS232")
    RS232_RATES = [110, 150, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]
    RS232_ERATEs = {"1": 0, "2": 0.005, "3": 0.01, "4": 0.02}

    def __init__(self) -> None:
        self._type = "V35"
        self._status = False #  default POWER OFF
        self._ebitrate: int = 64
        self._clockmode: str = None # remote если в режиме Slave, есть Internal и External
        self._clockdir: str = "CO" #contradirectional
        self._slotusage: bool = False #передача в КИ0 xDSL
        self._rs232bits: int = 8 # чекнуть
        self._rs232rate: int = 9600 # остальные выдают Got break signal  после DCD окна красного
        self._sigslots = {}  # чекнуть
        self._rs232erate: float = None

    @property
    def type(self):
        return self._type

    @property
    def ebitrate(self) -> int:
        return self._ebitrate
    
    @property
    def clockmode(self) -> str:
        return self._clockmode
    
    @property
    def clockdir(self) -> str:
        return self._clockdir
    
    @property
    def slotusage(self) -> bool:
        return self._slotusage
    
    @property
    def rs232bits(self) -> int:
        return self._rs232bits
    
    @property
    def rs232rate(self) -> int:
        return self._rs232rate
    
    @property
    def sigslots(self) -> Dict:
        return self._sigslots
    
    def set_type(self, type: str) -> None:
        if type not in Nx64.INTERFACES:
            return
        
        self._type = type
    
    def bitrate(self, N: int) -> None:
        if self._type == "RS232":
            print("для RS232 используйте команду RS232RATE")
            return

        # Таблица лимитов Nx64
        limits = {
           "V28": 3,
           "V35": 36,
           "V36_X21_WITHOUT_TERMINATION": 36, 
           "V36_X21_WITH_TERMINATION": 36
        }

        max_N = limits.get(self._type)
        if max_N is None:
            print(f"Неизвестный тип интерфейса: {self._type}")
            return

        if N < 1 or N > max_N:
            print(f"Максимум N = {max_N} для {self._type}")
            return

        self._bitrate = N * 64000

    def set_clockmode(self, mode: str) -> None:
        if mode not in ("EXT", "INT"):
            raise ValueError("CLOCKMODE должен быть INT(INTERNAL), EXT(EXTERNAL), REMOTE")
        # Если интерфейс slave, REMOTE только допустим
        if self._type != "RS232" and mode == "REMOTE":
            self._clockmode = "REMOTE"
        else:
            self._clockmode = mode

    def set_clockdir(self, direction: str) -> None:
        if direction not in ("CO", "CONTRA"):
            raise ValueError("CLOCKDIR должен быть CO или CONTRA")
        # Если CLOCKMODE = EXTERNAL, CONTRA недопустим
        if self._clockmode == "EXTERNAL" and direction == "CONTRA":
            print("Для EXTERNAL CLOCKDIR возможен только CO")
            self._clockdir = "CO"
        else:
            self._clockdir = direction

    def set_rs232rate(self, rate: int) -> None:
        if rate not in Nx64.RS232_RATES:
            raise ValueError(f"Недопустимая скорость RS232: {rate}")
        self._rs232rate = rate
    
    def set_rs232erate(self, value: int) -> None:
        if value not in Nx64.RS232_ERATEs:
            raise ValueError("1 - 4 ony")
        self._rs232erate = value

    def set_rs232bits(self, bits: int) -> None:
        if bits < 7 or bits > 10:
            raise ValueError("RS232BITS должно быть от 7 до 10")
        self._rs232bits = bits