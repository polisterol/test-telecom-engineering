import asyncio
import logging

async def handle_request(reader, writer):
    peername = writer.get_extra_info('peername')
    logging.info('Accepted connection from {}'.format(peername))

    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    logging.info('Received {} from {}'.format(message, addr))

    logging.info('Send: {}'.format(message))

    writer.write(data)
    await writer.drain()


    logging.info('Close the connection')
    writer.close()

async def main():
    logging.basicConfig(filename="debug.log", level=logging.INFO)
    server = await asyncio.start_server(handle_request, '', 2021)

    addr = server.sockets[0].getsockname()
    logging.info('Serving on {}'.format(addr))

    async with server:
        await server.serve_forever()

asyncio.run(main())