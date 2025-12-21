from typing import Dict

class Nx64:
    INTERFACES = {
        "0": "V.35",
        "1": "V.36/X.21 no term.",
        "2": "V.36/X.21 with term.",
        "3": "V.28",
        "4": "RS232"
    }

    RS232_RATES = [110, 150, 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]
    RS232_ERATES = {"1": 0, "2": 0.005, "3": 0.01, "4": 0.02}

    def __init__(self) -> None:
        # Дефолтные значения
        self._type: str = "V.35"          # интерфейс по умолчанию
        self._status: bool = False        # POWER OFF
        self._bitrate: int = 1
        self._ebitrate: int = 64
        self._clockmode: str = "internal" # internal по умолчанию
        self._clockdir: str = "CONTRA"    # contra
        self._role: str = "MASTER"        # MASTER по умолчанию
        self._slotusage: bool = False
        self._rs232bits: int = 8
        self._rs232_rate: int = 9600
        self._sigslots: Dict = {}
        self._rs232erate: float = 0
        self._rs232slot: int = 1

        self._rsr232ts = 1

        self._saved_clockmode: str = "internal" 

        self.adapt:bool = False


    # ---------- Properties ----------
    @property
    def saved_clockmode(self):
        return self._saved_clockmode

    @saved_clockmode.setter
    def saved_clockmode(self, value):
        self._saved_clockmode = value
    
    @property
    def clockmode(self) -> str:
        return self._clockmode

    @clockmode.setter
    def clockmode(self, value: str) -> None:
        self._clockmode = value


    @property
    def type(self) -> str:
        return self._type

    @property
    def ebitrate(self) -> int:
        return self._ebitrate

    @property
    def clockdir(self) -> str:
        return self._clockdir

    @property
    def role(self) -> str:
        return self._role

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

    # ---------- Methods ----------
    def set_type(self, type_key: str) -> None:
        self._type = self.INTERFACES.get(type_key, self._type)

    def set_clockmode(self, mode: str, role: str = "MASTER") -> None:
        self._role = role.upper()
        mode = mode.upper()

        if self._role == "SLAVE" and mode in ("EXT", "INT"):
            raise ValueError("Для SLAVE допустим только REMOTE режим")

        if mode == "REMOTE":
            self._clockmode = "remote"
        else:
            self._clockmode = mode.lower()  # internal/external

    def set_clockdir(self, direction: str) -> None:
        direction = direction.upper()
        if direction not in ("CO", "CONTRA"):
            raise ValueError("CLOCKDIR должен быть CO или CONTRA")

        if self._clockmode == "external" and direction == "CONTRA":
            print("Для EXTERNAL CLOCKDIR возможен только CO")
            self._clockdir = "CO"
        else:
            self._clockdir = direction

    def set_rs232rate(self, rate: int) -> None:
        if rate not in Nx64.RS232_RATES:
            raise ValueError(f"Недопустимая скорость RS232: {rate}")
        self._rs232rate = rate

    def set_rs232erate(self, value: str) -> None:
        if value not in Nx64.RS232_ERATES:
            raise ValueError("Допустимые значения: 1 - 4")
        self._rs232erate = value

    def set_rs232bits(self, bits: int) -> None:
        if bits < 7 or bits > 10:
            raise ValueError("RS232BITS должно быть от 7 до 10")
        self._rs232bits = bits

    def power_on(self) -> None:
        self._status = True

    def power_off(self) -> None:
        self._status = False
