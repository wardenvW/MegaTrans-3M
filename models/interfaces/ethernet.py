class Ethernet:
    def __init__(self):
        self._speed:str = "AUTO"
        self._duplex: str = "F" # H/F
        self._status: bool = False # у Nx64 и Ethener нужно Power ON чтобы они работали иначе они выключены 
        self.ethpayload: int = 1
    
    @property 
    def speed(self) -> str:
        return self._speed
    
    @property
    def duplex(self) -> str:
        return self._duplex
    
    def power_on(self) -> None:
        self._status = True

    def power_off(self) -> None:
        self._status = False