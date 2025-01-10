import asyncio
import time

import win32api
import win32con
import win32gui
from pymem import Pymem

# "PathOfExile.exe"+03886DB0
# 38  18 40 20 208 2c - MaxHP
# 38  18 40 20 208 30 - CurHP
# 38  18 40 20 208 7c - MaxMP
# 38  18 40 20 208 80 - CurMP

process_name = "PathOfExileSteam.exe"
pm = Pymem(process_name)
base_offset = 0x3B8FEE8
base_address = pm.base_address + base_offset
handle = win32gui.FindWindow(None, "Path of Exile 2")
offsets = {
    "CurHP": [0x70, 0x0, 0x80, 0x2A8, 0x1E0],
    "MaxHP": [0x70, 0x0, 0x80, 0x2A8, 0x1DC],  # 0x1E0 - 4
    "CurMP": [0x70, 0x0, 0x80, 0x2A8, 0x230],
    "MaxMP": [0x70, 0x0, 0x80, 0x2A8, 0x22C],  # 0x230 - 4
    "CurES": [0x70, 0x0, 0x80, 0x2A8, 0x268],
    "MaxES": [0x70, 0x0, 0x80, 0x2A8, 0x264],  # 0x268 - 4
}
# Heals %
hp_threshold = 60
mp_threshold = 70
es_threshold = 75
es_limit_threshold = 25


def get_final_address(pm: Pymem, base_address: int, offsets: list[int]) -> int:
    addr = pm.read_longlong(base_address)
    for offset in offsets[:-1]:
        addr = pm.read_longlong(addr + offset)
    return addr + offsets[-1]


async def hp_routine():
    while True:
        try:
            curhp_address = get_final_address(pm, base_address, offsets["CurHP"])
            # print(f"curhp_address: {curhp_address}")
            maxhp_address = get_final_address(pm, base_address, offsets["MaxHP"])
            # print(f"maxhp_address: {maxhp_address}")

            current_hp = pm.read_int(curhp_address)
            max_hp = pm.read_int(maxhp_address)

            hp_percent = (current_hp / max_hp) * 100 if max_hp != 0 else 0
            # print(f"HP: {current_hp} / {max_hp} ({hp_percent})")

            if hp_percent <= hp_threshold:
                win32api.PostMessage(handle, win32con.WM_KEYDOWN, ord("1"), 0)
                win32api.PostMessage(handle, win32con.WM_KEYUP, ord("1"), 0)
                current_time = time.strftime("%H:%M:%S")
                print(f"[{current_time}]: Used HP potion")
                await asyncio.sleep(0.5)
            await asyncio.sleep(0.2)
        except Exception as e:
            print(str(e))


async def mp_routine():
    while True:
        try:
            curmp_address = get_final_address(pm, base_address, offsets["CurMP"])
            # print(f"curmp_address: {curmp_address}")
            maxmp_address = get_final_address(pm, base_address, offsets["MaxMP"])
            # print(f"maxmp_address: {maxmp_address}")

            current_mp = pm.read_int(curmp_address)
            max_mp = pm.read_int(maxmp_address)

            mp_percent = (current_mp / max_mp) * 100 if max_mp != 0 else 0
            # print(f"MP: {current_mp} / {max_mp} ({mp_percent})")

            if mp_percent <= mp_threshold:
                win32api.PostMessage(handle, win32con.WM_KEYDOWN, ord("2"), 0)
                win32api.PostMessage(handle, win32con.WM_KEYUP, ord("2"), 0)
                current_time = time.strftime("%H:%M:%S")
                print(f"[{current_time}]: Used MP potion")
                await asyncio.sleep(0.5)
            await asyncio.sleep(0.2)
        except Exception as e:
            print(str(e))

async def es_routine():
    while True:
        try:
            cures_address = get_final_address(pm, base_address, offsets["CurES"])
            maxes_address = get_final_address(pm, base_address, offsets["MaxES"])

            current_es = pm.read_int(cures_address)
            max_es = pm.read_int(maxes_address)

            es_percent = (current_es / max_es) * 100 if max_es != 0 else 0
            # print(f"ES: {current_es} / {max_es} ({es_percent})")

            if es_percent <= es_threshold:
                win32api.PostMessage(handle, win32con.WM_KEYDOWN, ord("1"), 0)
                win32api.PostMessage(handle, win32con.WM_KEYUP, ord("1"), 0)
                current_time = time.strftime("%H:%M:%S")
                print(f"[{current_time}]: Used HP potion for ES + Eternal Youth")
                await asyncio.sleep(0.5)
            await asyncio.sleep(0.2)
        except Exception as e:
            print(str(e))

async def es_limit_routine():
    while True:
        try:
            cures_address = get_final_address(pm, base_address, offsets["CurES"])
            maxes_address = get_final_address(pm, base_address, offsets["MaxES"])

            current_es = pm.read_int(cures_address)
            max_es = pm.read_int(maxes_address)

            es_percent = (current_es / max_es) * 100 if max_es != 0 else 0
            # print(f"ES limit: {current_es} / {max_es} ({es_percent})")
            wait_in_sec = 120

            if es_percent <= es_limit_threshold:
                win32api.PostMessage(handle, win32con.WM_KEYDOWN, 0x1B, 0)
                # win32api.PostMessage(handle, win32con.WM_KEYUP, 0x1B, 0)
                current_time = time.strftime("%H:%M:%S")
                print(f"[{current_time}]: ESC pressed on limit {es_percent} with {wait_in_sec} sec. Time to action!")
                await asyncio.sleep(wait_in_sec)
            await asyncio.sleep(0.2)
        except Exception as e:
            print(str(e))


async def main():
    async with asyncio.TaskGroup() as tg:
        print(f"Autoheal is ON")
        tg.create_task(hp_routine())
        tg.create_task(mp_routine())
        tg.create_task(es_routine())
        tg.create_task(es_limit_routine())


if __name__ == "__main__":
    asyncio.run(main())
