from typing import Tuple, Any, Optional, Union

class E1:
    def __init__(self) -> None:
        self._g704: bool = True
        self._crc4: bool = True
        self._ebit: bool = True   
        self._aisgen: bool = False
        self._aisdet: bool = False
        self._extclk: bool = False
        self._pcm: Tuple[int, bool, Any] = (31, False, None)
        self._idlecas = None
        self._idlepat: int = 0xFF
        self._signal_slot: Union[None, str, Tuple[int, int]] = None
    
    @property
    def g704(self) -> bool:
        return self._g704
    
    @property
    def signal_slot(self) -> Union[None, str, Tuple[int, int]]:
        return self._signal_slot
    
    @property
    def crc4(self) -> bool:
        return self._crc4
    
    @property
    def ebit(self) -> bool:
        return self._ebit
    
    @property
    def aisgen(self) -> bool:
        return self._aisgen
    
    @property 
    def aisdet(self) -> bool:
        return self._aisdet
    
    @property
    def extclk(self) -> bool:
        return self._extclk
    
    @property
    def pcm(self) -> Tuple[int, bool, Any]:
        return self._pcm
    
    @property
    def idlecas(self) -> int:
        return self._idlecas
    
    @property
    def idlepat(self) -> int:
        return self._idlepat
    
    def g704_turn_off(self) -> None:
        self._g704 = False
        self._crc4 = False
        self._ebit = False

    def g704_turn_on(self) -> None:
        self._g704 = True
        self._crc4 = True
        self._ebit = True

    def crc4_turn_off(self) -> None:
        self._crc4 = False
        self._ebit = False

    def crc4_turn_on(self) -> None:
        if self._g704:
            self._crc4 = True

    def ebit_turn_off(self) -> None:
        self._ebit = False

    def ebit_turn_on(self) -> None:
        if self._g704 and self._crc4: 
            self._ebit = True

    def aisgen_turn_off(self) -> None:
        self._aisgen = False  

    def aisgen_turn_on(self) -> None:
        self._aisgen = True

    def aisdet_turn_off(self) -> None:
        self._aisdet = False

    def aisdet_turn_on(self) -> None:
        self._aisdet = True

    def extclk_turn_off(self) -> None: 
        self._extclk = False

    def extclk_turn_on(self) -> None:  
        self._extclk = True

    def change_pcm(self, value: int, extra) -> None:
        if value == 31:
            self._pcm = (31, False, None)
            # В режиме PCM31 сигнализация не используется
            self._idlecas = None
        elif value == 30:
            self._pcm = (30, True, extra)
            self._idlecas = 0xD  # Дефолтная сигнализация для PCM30
        else:
            raise ValueError("PCM может быть только 30 или 31")

    def set_idlecas(self, value_hex: str) -> None:
        try:
            value = int(value_hex, 16)
        except ValueError:
            raise ValueError("Idle CAS должен быть HEX значением (0–F)")

        if not (0x0 <= value <= 0xF):
            raise ValueError("Idle CAS должен быть в диапазоне 0x0 - 0xF")

        if self._pcm[0] == 30: 
            self._idlecas = value
        else:
            raise TypeError("Idle CAS можно установить только в режиме PCM30")



    def set_idlepat(self, value_hex: str) -> None:
        try:
            value = int(value_hex, 16)
        except ValueError:
            raise ValueError("Idle CAS должен быть HEX значением (0 - F)")

        if not (0x0 <= value <= 0xF):
            raise ValueError("Idle CAS должен быть в диапазоне 0 - F")

        if self._pcm[0] == 30:
            self._idlepat = value
        else:
            raise TypeError("Idle CAS можно установить только в режиме PCM30")