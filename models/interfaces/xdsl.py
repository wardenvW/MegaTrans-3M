class xDSL:
    def __init__(self):
        self.active: bool = False
        self.queue: list = []  # порядок передачи: ["E1", "Nx64", "Ethernet"]
        self.e1_slots: list = []
        self.nx64_slots: list = []
        self.eth_packets: list = []
        self.max_bitrate: int = {""}  # кбит/с
        self.bitrate: str = "0584"
        self.pll: bool = False

        self.base_rate:int = 0

        self.use_time_slot_0: bool = False
        self.auto_restart: bool = True
        self.adapt = True
        self.scale:float = 0
        
        self.startup: bool = False
        self.annex: str = "A"
        self.snr: float = 34.2
