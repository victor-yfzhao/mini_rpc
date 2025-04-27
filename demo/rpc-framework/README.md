# RPC Framework

This project implements a simple Remote Procedure Call (RPC) framework that allows clients to invoke methods on a remote server as if they were local calls. The framework includes a calculator service with basic arithmetic operations.

## Project Structure

```
rpc-framework
├── src
│   ├── server
│   │   ├── __init__.py
│   │   ├── calculator_service.py
│   │   └── server.py
│   ├── client
│   │   ├── __init__.py
│   │   ├── calculator_stub.py
│   │   └── client.py
│   ├── protocol
│   │   ├── __init__.py
│   │   └── protocol.py
│   └── types
│       └── __init__.py
├── requirements.txt
└── README.md
```

## Features

- **Calculator Service**: Provides methods for basic arithmetic operations:
  - `add(int a, int b)`
  - `subtract(int a, int b)`

- **Client-Server Model**: Implements a TCP server that listens for client connections and processes requests.

- **Serialization/Deserialization**: Handles the conversion of requests and responses into a format suitable for network transmission.

## Getting Started

### Requirements

Make sure you have Python installed. You can install the required dependencies using:

```
pip install -r requirements.txt
```

### Running the Server

To start the server, navigate to the `src/server` directory and run:

```
python server.py
```

### Running the Client

To use the client, navigate to the `src/client` directory and run:

```
python client.py
```

You can call the calculator methods through the client, which will communicate with the server to perform the operations.

## Future Enhancements

- Support for additional data types (e.g., floats, strings, lists).
- Exception handling and error reporting.
- Concurrent handling of multiple client requests.
- Service registration and discovery mechanisms.

## License

This project is open-source and available under the MIT License.