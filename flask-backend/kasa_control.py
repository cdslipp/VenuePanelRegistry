# flask-backend/kasa_control.py

from kasa import SmartPlug, SmartDeviceException
import asyncio

# Kasa smart plug IP addresses
STAGE_RIGHT_PLUG_IP = "192.168.0.51"
STAGE_LEFT_PLUG_IP = "192.168.0.52"

async def turn_on_work_lights():
    stage_right_plug = SmartPlug(STAGE_RIGHT_PLUG_IP)
    stage_left_plug = SmartPlug(STAGE_LEFT_PLUG_IP)

    try:
        # Turn on stage right plug
        await stage_right_plug.update()  # Fetch the current state from the plug
        if not stage_right_plug.is_on:
            await stage_right_plug.turn_on()

        # Turn on stage left plug
        await stage_left_plug.update()  # Fetch the current state from the plug
        if not stage_left_plug.is_on:
            await stage_left_plug.turn_on()
        return None  # No error
    except SmartDeviceException:
        return "Failed to connect to the Kasa device."

async def turn_off_work_lights():
    stage_right_plug = SmartPlug(STAGE_LEFT_PLUG_IP)
    stage_left_plug = SmartPlug(STAGE_LEFT_PLUG_IP)

    try:
        # Turn off stage right plug
        await stage_right_plug.update()  # Fetch the current state from the plug
        if stage_right_plug.is_on:
            await stage_right_plug.turn_off()

        # Turn off stage left plug
        await stage_left_plug.update()  # Fetch the current state from the plug
        if stage_left_plug.is_on:
            await stage_left_plug.turn_off()
        return None  # No error
    except SmartDeviceException:
        return "Failed to connect to the Kasa device."

async def get_work_lights_state():
    stage_right_plug = SmartPlug(STAGE_RIGHT_PLUG_IP)
    stage_left_plug = SmartPlug(STAGE_LEFT_PLUG_IP)

    try:
        await stage_right_plug.update()
        await stage_left_plug.update()

        # Return whether any of the work lights (plugs) is turned on
        return stage_right_plug.is_on or stage_left_plug.is_on, None  # No error
    except SmartDeviceException:
        return None, "Failed to connect to the Kasa device."
