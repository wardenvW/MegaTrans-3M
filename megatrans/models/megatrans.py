class Megatrans:
    def __init__(self, port_id: int) -> None:
        self._id = port_id
        self._status: bool = False  # Power OFF по умолчанию

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def status(self) -> bool:
        return self._status


    def turn_on(self) -> None:
        self._status = True
    
    def turn_off(self) -> None:
        self._status = False

    def __str__(self) -> str:
        return f"Megatrans[COM{self._id}, status={'ON' if self._status else 'OFF'}]"