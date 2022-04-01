from discord import Colour


class Colors(Colour):
    """Custom Color class"""

    # /statistics
    @classmethod
    def royal_blue(cls):
        """0x6600ff"""
        return cls(0x6600ff)

    # /ping
    @classmethod
    def sea_green(cls):
        """0x45bf55"""
        return cls(0x45bf55)

    # Command Errors
    @classmethod
    def black(cls):
        """0x000000"""
        return cls(0x000000)

    # /about
    @classmethod
    def neon_blue(cls):
        """0x15f4ee"""
        return cls(0x15f4ee)

    @classmethod
    def moon(cls):
        """0xcacaca"""
        return cls(0xcacaca)

    @classmethod
    def mars(cls):
        """0x9c2e35"""
        return cls(0x9c2e35)

    @classmethod
    def violet(cls):
        """0x0b5d85"""
        return cls(0x0b5d85)

    @classmethod
    def iss(cls):
        """0x6c6d7a"""
        return cls(0x6c6d7a)
