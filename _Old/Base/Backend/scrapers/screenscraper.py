import requests

gameUrl = "https://www.screenscraper.fr/api2/jeuInfos.php?devid=muldjord&devpassword=uWu5VRc9QDVMPpD8&softname=skyscraper"



class ScreenScraper:
    def __init__(self):
        pass
    


    def getPlatformID(self,platform):
        if platform.lower() == "3do":
            return "29"
        elif platform.lower() == "3ds":
            return "17"
        elif platform.lower() == "amiga":
            return "64"
        elif platform.lower() == "aga":
            return "111"
        elif platform.lower() == "cd32":
            return "130"
        elif platform.lower() == "cdtv":
            return "129"
        elif platform.lower() == "amstradcpc":
            return "65"
        elif platform.lower() == "apple2":
            return "86"
        elif platform.lower() == "arcade":
            return "75"
        elif platform.lower() == "arcadia":
            return "94"
        elif platform.lower() == "astrocde":
            return "44"
        elif platform.lower() == "atari800":
            return "43"
        elif platform.lower() == "atari2600":
            return "26"
        elif platform.lower() == "atari5200":
            return "40"
        elif platform.lower() == "atari7800":
            return "41"
        elif platform.lower() == "atarijaguar":
            return "27"
        elif platform.lower() == "atarijaguarcd":
            return "171"
        elif platform.lower() == "atarilynx":
            return "28"
        elif platform.lower() == "atarist":
            return "42"
        elif platform.lower() == "atomiswave":
            return "75"
        elif platform.lower() == "c16":
            return "na"
        elif platform.lower() == "c64":
            return "66"
        elif platform.lower() == "c128":
            return "na"
        elif platform.lower() == "channelf":
            return "80"
        elif platform.lower() == "coco":
            return "144"
        elif platform.lower() == "coleco":
            return "48"
        elif platform.lower() == "daphne":
            return "49"
        elif platform.lower() == "dragon32":
            return "91"
        elif platform.lower() == "dreamcast":
            return "23"
        elif platform.lower() == "easyrpg":
            return "231"
        elif platform.lower() == "fba":
            return "75"
        elif platform.lower() == "fds":
            return "106"
        elif platform.lower() == "gameandwatch":
            return "52"
        elif platform.lower() == "gamegear":
            return "21"
        elif platform.lower() == "gb":
            return "9"
        elif platform.lower() == "gba":
            return "12"
        elif platform.lower() == "gbc":
            return "10"
        elif platform.lower() == "gc":
            return "13"
        elif platform.lower() == "genesis":
            return "1"
        elif platform.lower() == "intellivision":
            return "115"
        elif platform.lower() == "mame-advmame":
            return "75"
        elif platform.lower() == "mame-libretro":
            return "75"
        elif platform.lower() == "mame-mame4all":
            return "75"
        elif platform.lower() == "mastersystem":
            return "2"
        elif platform.lower() == "megacd":
            return "20"
        elif platform.lower() == "megadrive":
            return "1"
        elif platform.lower() == "moto":
            return "141"
        elif platform.lower() == "msx":
            return "113"
        elif platform.lower() == "msx2":
            return "113"
        elif platform.lower() == "n64":
            return "14"
        elif platform.lower() == "naomi":
            return "75"
        elif platform.lower() == "nds":
            return "15"
        elif platform.lower() == "neogeo":
            return "142"
        elif platform.lower() == "neogeocd":
            return "70"
        elif platform.lower() == "nes":
            return "3"
        elif platform.lower() == "ngp":
            return "25"
        elif platform.lower() == "ngpc":
            return "82"
        elif platform.lower() == "openbor":
            return "214"
        elif platform.lower() == "oric":
            return "131"
        elif platform.lower() == "pc":
            return "135"
        elif platform.lower() == "pc88":
            return "na"
        elif platform.lower() == "pc98":
            return "208"
        elif platform.lower() == "pcfx":
            return "72"
        elif platform.lower() == "pcengine":
            return "31"
        elif platform.lower() == "pcenginecd":
            return "114"
        elif platform.lower() == "pokemini":
            return "211"
        elif platform.lower() == "ports":
            return "135"
        elif platform.lower() == "ps2":
            return "58"
        elif platform.lower() == "psp":
            return "61"
        elif platform.lower() == "psx":
            return "57"
        elif platform.lower() == "saturn":
            return "22"
        elif platform.lower() == "scummvm":
            return "123"
        elif platform.lower() == "sega32x":
            return "19"
        elif platform.lower() == "segacd":
            return "20"
        elif platform.lower() == "sg-1000":
            return "109"
        elif platform.lower() == "snes":
            return "4"
        elif platform.lower() == "switch":
            return "225"
        elif platform.lower() == "ti99":
            return "205"
        elif platform.lower() == "trs-80":
            return "144"
        elif platform.lower() == "vectrex":
            return "102"
        elif platform.lower() == "vic20":
            return "73"
        elif platform.lower() == "videopac":
            return "104"
        elif platform.lower() == "virtualboy":
            return "11"
        elif platform.lower() == "wii":
            return "16"
        elif platform.lower() == "wiiu":
            return "18"
        elif platform.lower() == "wonderswan":
            return "45"
        elif platform.lower() == "wonderswancolor":
            return "46"
        elif platform.lower() == "x68000":
            return "79"
        elif platform.lower() == "x1":
            return "na"
        elif platform.lower() == "zmachine":
            return "na"
        elif platform.lower() == "zx81":
            return "77"
        elif platform.lower() == "zxspectrum":
            return "76"
        else:
            return "na"
