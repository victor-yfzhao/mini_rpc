# mini_rpc

一个基于 Python 的轻量级 RPC 框架，支持服务发现与广播，基于 Protobuf 进行消息序列化，适合快速开发分布式服务。

## 特性

- 基于 TCP 的高效通信
- 支持服务自动发现与广播（UDP）
- 使用 Protocol Buffers 进行消息定义与序列化
- 支持自定义服务与方法注册
- 简单易用的客户端/服务端接口

## 目录结构

```
mini-rpc/
├── example/                # 示例：计算器服务与客户端
│   └── calculator/
│       ├── calculator_server.py
│       ├── calculator_client.py
│       ├── calculator_stub.py
│       └── messages/
│           ├── calculator_messages.proto
│           └── calculator_messages_pb2.py
├── src/
│   ├── client_stub/        # 客户端存根
│   ├── server/             # 服务端基类
│   ├── service_announcer.py
│   ├── service_discovery.py
│   └── template/           # 通用消息模板
│       ├── template_message.proto
│       └── template_message_pb2.py
└── README.md
```

## 依赖

- Python 3.7+
- `protobuf` >= 4.25.3

安装依赖：
```bash
pip install protobuf
```

## 快速开始

### 1. 启动服务端

```bash
python example/launch_server.py
```

### 2. 启动客户端

```bash
python example/launch_clients.py
```

### 3. 示例输出

客户端会自动发现服务并进行加减乘除等远程调用。

## 协议说明

- 服务端与客户端通过 Protobuf 定义的消息进行通信，见 `src/template/template_message.proto`。
- 支持通过 UDP 广播自动发现服务，无需手动配置 IP。

## 自定义服务

1. 定义自己的 Protobuf 消息。
2. 继承 `MiniRpcServer`，通过`super.register_service()`注册方法，并实现`call_method()`方法。
3. 实现客户端存根，继承 `MiniRpcStub`，通过`super.call()`进行远程调用。

## License

Apache 2.0