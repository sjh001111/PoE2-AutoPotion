import time
import win32api
import win32con
import win32gui
from pymem import Pymem
from time import sleep
import asyncio

# "PathOfExile.exe"+03886DB0
# 38  18 40 20 208 2c - MaxHP
# 38  18 40 20 208 30 - CurHP
# 38  18 40 20 208 7c - MaxMP
# 38  18 40 20 208 80 - CurMP

process_name = "PathOfExileSteam.exe"
pm = Pymem(process_name)
base_offset = 0x03B8DE78
base_address = pm.base_address + base_offset
handle = win32gui.FindWindow(None, "Path of Exile 2")
offsets = {
    "CurHP": [0x38, 0x0, 0x80, 0x2A8, 0x1E0],
    "MaxHP": [0x38, 0x0, 0x80, 0x2A8, 0x1DC],  # 0x1E0 - 4
    "CurMP": [0x38, 0x0, 0x80, 0x2A8, 0x230],
    "MaxMP": [0x38, 0x0, 0x80, 0x2A8, 0x22C],  # 0x230 - 4
}
# Heals %
hp_threshold = 60
mp_threshold = 15


def get_final_address(pm: Pymem, base_address: int, offsets: list[int]) -> int:
    addr = pm.read_longlong(base_address)
    for offset in offsets[:-1]:
        addr = pm.read_longlong(addr + offset)
    return addr + offsets[-1]


async def hp_routine():
    while True:
        try:
            curhp_address = get_final_address(pm, base_address, offsets["CurHP"])
            maxhp_address = get_final_address(pm, base_address, offsets["MaxHP"])

            current_hp = pm.read_int(curhp_address)
            max_hp = pm.read_int(maxhp_address)

            hp_percent = (current_hp / max_hp) * 100 if max_hp != 0 else 0
            print(f"HP: {current_hp} / {max_hp} ({hp_percent})")

            if hp_percent <= hp_threshold:
                print("Use HP potion")
                win32api.PostMessage(handle, win32con.WM_KEYDOWN, ord("1"), 0)
                win32api.PostMessage(handle, win32con.WM_KEYUP, ord("1"), 0)
                await asyncio.sleep(0.5)
            await asyncio.sleep(0.2)
        except Exception as e:
            print(str(e))


async def mp_routine():
    while True:
        try:
            curmp_address = get_final_address(pm, base_address, offsets["CurMP"])
            maxmp_address = get_final_address(pm, base_address, offsets["MaxMP"])

            current_mp = pm.read_int(curmp_address)
            max_mp = pm.read_int(maxmp_address)

            mp_percent = (current_mp / max_mp) * 100 if max_mp != 0 else 0
            print(f"MP: {current_mp} / {max_mp} ({mp_percent})")


            if mp_percent <= mp_threshold:
                print("Use MP potion")
                win32api.PostMessage(handle, win32con.WM_KEYDOWN, ord("2"), 0)
                win32api.PostMessage(handle, win32con.WM_KEYUP, ord("2"), 0)
                await asyncio.sleep(0.5)
            await asyncio.sleep(0.2)
        except Exception as e:
            print(str(e))


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(hp_routine())
        tg.create_task(mp_routine())


if __name__ == "__main__":
    asyncio.run(main())
