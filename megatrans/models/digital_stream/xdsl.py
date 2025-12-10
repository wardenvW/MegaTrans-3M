class xDSL:
    def __init__(self, id: int):
        self.id = id
        self.active: bool = False
        self.queue: list = []  # порядок передачи: ["E1", "Nx64", "Ethernet"]
        self.e1_slots: list = []
        self.nx64_slots: list = []
        self.eth_packets: list = []
        self.max_bitrate: int = {""}  # кбит/с
        self.bitrate: int = 0

    def set_service_queue(self, *args):
        """Задает порядок передачи интерфейсов"""
        self.queue = list(args)

    def calculate_bitrate(self):
        """Рассчитывает реальный битрейт с учетом порядка SERVICE"""
        br = 0
        remaining = self.max_bitrate
        for iface in self.queue:
            if iface == "E1" and self.e1_slots:
                needed = len(self.e1_slots) * 64
                allocated = min(needed, remaining)
                br += allocated
                remaining -= allocated
            elif iface == "Nx64" and self.nx64_slots:
                needed = len(self.nx64_slots) * 64
                allocated = min(needed, remaining)
                br += allocated
                remaining -= allocated
            elif iface == "Ethernet" and self.eth_packets:
                needed = sum(len(p)*8//1000 for p in self.eth_packets)  # кбит
                allocated = min(needed, remaining)
                br += allocated
                remaining -= allocated
            if remaining <= 0:
                break
        self.bitrate = br