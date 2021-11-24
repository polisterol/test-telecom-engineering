import asyncio
import logging
import re
import pendulum

async def handle_request(reader, writer):
    peername = writer.get_extra_info('peername')
    logging.info('Accepted connection from {}'.format(peername))

    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    logging.info('Received {} from {}'.format(message, addr))

    response = 'Message format does not match BBBBxNNxHH:MM:SS.zhqxGGCR'

    match = re.search(r"^(\d\d\d\d) ([a-zA-z0-9]{2}) (\d\d:\d\d:\d\d\.\d\d\d) (\d\d)\s?$", message)

    if match:

        try:
            athlete_time = pendulum.parse(match.group(3))

        except ValueError as err:
            response = "Time error: {}".format(err)
            logging.error(response)

        else:
            response = 'Спортсмен, нагрудный номер {} прошёл отсечку {} в «{}»\n'.format( match.group(1), match.group(2), athlete_time.format('H:m:s.S') )

            with open('metrics.log', 'a') as f:
                f.write(response)

            if match.group(4) == "00":
                logging.info('Response: {}'.format(response))
                writer.write(response.encode())
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