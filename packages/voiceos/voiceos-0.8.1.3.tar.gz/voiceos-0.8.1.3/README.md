# VoiceOS Python SDK

This python client lets you build with [VoiceOS](https://voiceos.io)

## Installation

You can install the package via pip:

```bash
pip install voiceos
```

## Usage

Import the VoiceOS class from the package:

```python
from voiceos.client import VoiceOS
```

Create a new instance of the VoiceOS class by passing your API key:

```python
voiceos = VoiceOS("your-api-key")
```

Start using the python client to access the [agent](https://docs.voiceos.io/api-reference/agents/get), [calls](https://docs.voiceos.io/api-reference/conversations/get) and [phone numbers](https://docs.voiceos.io/api-reference/phone-numbers/get) resources.

```python
# Get all agents
agents = voiceos.agents.list_agents()
print(agents)

# Get all calls
calls = voiceos.conversations.list_conversations()
print(calls)

# Get all phone numbers
phone_numbers = voiceos.phone_numbers.list_phone_numbers()
print(phone_numbers)
```

## License

```
MIT License

Copyright (c) 2024 WakoAI Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```