import time

import click

from mira_edge.mira_edge import MiraEdge
from mira_edge.mira_protocol import Frame
from mira_edge.model import EdgeEvent, MiraNode
from mira_edge.tui import MiraEdgeTUI


def on_event(event: EdgeEvent, event_data: MiraNode | Frame):
    if event == EdgeEvent.NODE_JOINED:
        assert isinstance(event_data, MiraNode)
        # print(f"Node {event_data} joined")
        # print("#", end="", flush=True)
    elif event == EdgeEvent.NODE_LEFT:
        assert isinstance(event_data, MiraNode)
        # print(f"Node {event_data} left")
        # print("0", end="", flush=True)
    elif event == EdgeEvent.NODE_DATA:
        assert isinstance(event_data, Frame)
        # print(f"Got frame from 0x{event_data.header.source:016x}: {event_data.payload.hex()}")
        # print(".", end="", flush=True)


@click.command()
@click.option('--port', '-p', help='Serial port to use (e.g., /dev/ttyUSB0)')
def main(port: str | None):
    """Basic example of using MiraEdge to communicate with nodes."""
    mira = MiraEdge(on_event=on_event, port=port)
    tui = MiraEdgeTUI()

    try:
        mira.connect_to_gateway()

        while True:
            mira.send_frame(dst=0xFF, payload=b"A" * 32)
            for node in mira.gateway.nodes:
                # print(f"Sending frame to 0x{node.address:016x}")
                mira.send_frame(dst=node.address, payload=b"A" * 32)
            time.sleep(0.3)
            # tui.render(mira)

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        tui.close()
        mira.disconnect_from_gateway()


if __name__ == '__main__':
    main()
