from tools.api import send_group_msg
import asyncio
async def main():
    await send_group_msg(1057162186, "test")
asyncio.run(main())