# Sentinel OS - Interactive Demo

This repository contains an interactive demo for **Sentinel OS**, the control plane for agentic AI systems. It demonstrates how Sentinel OS can detect and prevent attacks on AI agents in real time.

## 🚀 Live Demo

Try the interactive demo here:
👉 [https://yourusername.github.io/sentinel-os-demo](https://yourusername.github.io/sentinel-os-demo)

## 🛡️ What is Sentinel OS?

Sentinel OS is a security and governance layer for AI agents. It:
- ✅ Approves safe actions
- ✅ Blocks malicious behavior
- ✅ Logs every decision
- ✅ Simulates attacks before production

## 🧪 Demo Overview

This demo simulates an attack on a LangChain agent:
1. The agent receives a prompt (safe or malicious).
2. Sentinel OS analyzes the action in real time.
3. If the action is safe, it is executed. If malicious, it is blocked.

### Try It Yourself
- **Safe Example**: `Get customer data for 1`
- **Attack Example**: `Get customer data for 1; DROP TABLE customers;`

## 📦 Installation

To integrate Sentinel OS into your own agents:

```bash
pip install sentinel-os
```

## 🔧 Usage

See the [examples](examples/) directory for usage examples, including:
- Basic usage
- LangChain integration
- Attack simulation

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for more details.

## 📜 License

MIT