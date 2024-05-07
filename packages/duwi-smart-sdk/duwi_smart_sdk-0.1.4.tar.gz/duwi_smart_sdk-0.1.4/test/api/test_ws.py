from unittest import TestCase
from duwi_smart_sdk.api.ws import DeviceSynchronizationWS
import asyncio


class TestDeviceSynchronizationWS(TestCase):
    def test_device_synchronization(self):
        async def run_test():
            async def on_callback(x: str):
                print(f"on_callback: {x}")

            ws = DeviceSynchronizationWS(
                on_callback=on_callback,
                app_key="2e479831-1fb7-751e-7017-7534f7f99fc1",
                app_secret="26af4883a943083a4c34083897fcea10",
                access_token="715d1c63-85c0-4d74-9a89-5a0aa4806f74",
                refresh_token="c539ec1b-99d9-44f2-8bb0-b942545c0aca",
                house_no="c7bf567d-225a-4533-ab72-5dc080b794f5",
                app_version="0.0.1",
                client_version="0.0.1",
                client_model="homeassistant",
            )

            await ws.reconnect()
            await ws.listen()
            await ws.keep_alive()

        asyncio.run(run_test())
