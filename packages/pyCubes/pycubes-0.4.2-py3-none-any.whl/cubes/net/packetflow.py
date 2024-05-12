import enum


class PacketFlow(enum.Enum):
    CLIENTBOUND = "clientbound"
    SERVERBOUND = "serverbound"
