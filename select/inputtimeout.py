import sys
import select
import termios

DEFAULT_TIMEOUT = 2

LF = '\n'


def echo(string):
    sys.stdout.write(string)
    sys.stdout.flush()


class TimeoutExpired(Exception):
    pass


def input_timeout(prompt='', timeout=DEFAULT_TIMEOUT):
    echo(prompt)
    readable, _, _ = select.select([sys.stdin], [], [], timeout)

    for stdin in readable:
        return stdin.readline().rstrip(LF)
    else:
        echo(LF)
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        raise TimeoutExpired


if __name__ == '__main__':
    try:
        while True:
            try:
                answer = input_timeout('Input:', 2)
            except TimeoutExpired:
                print('Timeout.!')
                continue
            else:
                print(f'Received: {answer}')
    except KeyboardInterrupt:
        'Stop'
        pass
