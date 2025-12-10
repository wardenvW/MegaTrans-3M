class Ethernet:
    def __init__(self):
        self._speed:str = " AUTO ili 10 ili 100 esli AUTo то автоматически распределяем, остальное int(_speed)"
        self._duplex: str = None # H/F
        self._status: bool = False # у Nx64 и Ethener нужно Power ON чтобы они работали иначе они выключены 
    
    @property 
    def speed(self) -> str:
        return self._speed
    
    @property
    def duplex(self) -> str:
        return self._duplex
    
    def ethernet_speed_duplex(self, speed: str, duplex: str) -> None:
        if speed == "AUTO":
            self._speed = speed
            self._duplex = "F"
            return
        
        self._speed = speed
        self._duplex = duplex