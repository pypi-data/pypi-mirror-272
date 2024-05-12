import asyncio
import time
from ....Domain.Shared.Utils.logger import _logger

async def call_flutter_code_gen(app_name: str):
    time.sleep(30)
    await asyncio.gather(
        run(f"flutter pub run build_runner build", cwd=app_name),
        run(f"flutter run -d chrome", cwd=app_name),
    )

async def run(cmd, cwd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')