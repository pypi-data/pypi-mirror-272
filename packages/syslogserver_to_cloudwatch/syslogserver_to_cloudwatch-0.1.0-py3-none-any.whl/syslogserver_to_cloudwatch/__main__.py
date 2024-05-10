import asyncio
from datetime import datetime, timezone
from functools import cache, partial
import os
import sys
import time
from operator import itemgetter

import boto3

cloudwatch_logs = boto3.client("logs")
BULK_MESSAGES = 1000
PORT = int(os.getenv("PORT", "5140"))
CLOUDWATCH_LOG_GROUP = os.getenv("CLOUDWATCH_LOG_GROUP")
CLOUDWATCH_LOG_STREAM = f"syslogserver-to-cloudwatch/{datetime.now(timezone.utc):%Y-%m-%d-%H-%M-%S}"

if CLOUDWATCH_LOG_GROUP is None:
    print(
        "CLOUDWATCH_LOG_GROUP environment variable not set, could not start server",
        file=sys.stderr,
    )
    sys.exit(1)

print(f"{CLOUDWATCH_LOG_GROUP=}")
print(f"{CLOUDWATCH_LOG_STREAM=}")

cloudwatch_logs.create_log_stream(
    logGroupName=CLOUDWATCH_LOG_GROUP,
    logStreamName=CLOUDWATCH_LOG_STREAM,
)


class CloudwatchLogsUDPProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue: list):
        self.queue = queue

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data[4:-1].decode()

        self.queue.append(
            {
                "timestamp": int(time.time() * 1000),
                "message": message,
            }
        )


async def process_queue(*, queue: list):
    loop = asyncio.get_running_loop()
    while True:
        while queue:
            messages = [queue.pop() for _ in range(min(BULK_MESSAGES, len(queue)))]
            messages = sorted(messages, key=itemgetter("timestamp"))
            await loop.run_in_executor(
                None,
                partial(
                    cloudwatch_logs.put_log_events,
                    logGroupName=CLOUDWATCH_LOG_GROUP,
                    logStreamName=CLOUDWATCH_LOG_STREAM,
                    logEvents=messages,
                ),
            )
            print(f"Sent messages: {len(messages)}, messages remaining: {len(queue)}")
        await asyncio.sleep(1)


async def run_server():
    print(f"Starting UDP server on port {PORT}")
    loop = asyncio.get_running_loop()
    queue = []
    transport, _ = await loop.create_datagram_endpoint(
        lambda: CloudwatchLogsUDPProtocol(queue),
        local_addr=("0.0.0.0", PORT),
    )

    try:
        await process_queue(queue=queue)
    finally:
        print("Closing server")
        transport.close()


def main():
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
