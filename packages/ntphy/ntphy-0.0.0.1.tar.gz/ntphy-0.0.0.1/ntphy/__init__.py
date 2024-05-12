from ntphy.utils.messages import Messages as _messages
from ntphy.utils.output import Output as _output
from ntphy.utils.server import Server as _server
from threading import Thread as _thread

def connect():
    output = _output()
    messages = _messages(output)
    server = _server()

    output.initial_connection()

    # Process each subscription in its own thread
    threads = []
    for name, url in server.subscriptions_dict().items():
        thread = _thread(target=messages.filter_message, args=(name, url))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()