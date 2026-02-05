# Multi Upload Tool - Python SDK

Official Python SDK for [Multi Upload Tool](https://multi-upload-tool.com) — upload videos and images to TikTok, YouTube, Instagram, Facebook, Pinterest and more from a single API call.

## Install

```bash
pip install multi-upload-tool
```

Requires Python 3.8+.

## Quick Start

```python
from multi_upload_tool import MultiUploadClient

client = MultiUploadClient(api_token="your-api-token")

# Upload a video
upload = client.uploads.upload(
    account_id=123,
    file_path="/path/to/video.mp4",
    title="My Video",
)

# Bulk upload to multiple accounts at once
accounts = client.accounts.list(status="active")
client.uploads.upload(
    account_id=[a["id"] for a in accounts],
    file_path="/path/to/video.mp4",
    title="Goes everywhere",
)

client.close()
```

## Features

- Upload to TikTok, YouTube, Instagram, Facebook, Pinterest
- Bulk upload to multiple accounts in one call
- Image carousels
- Scheduled uploads
- Short links, webhooks, teams, white label

## Documentation

Full SDK reference: [docs.multi-upload-tool.com/sdk/python](https://docs.multi-upload-tool.com/sdk/python)

API docs: [docs.multi-upload-tool.com/api-reference](https://docs.multi-upload-tool.com/api-reference)

## Links

- [Multi Upload Tool](https://multi-upload-tool.com) — Post More. Grow More. Earn More.
- [Dashboard](https://app.multi-upload-tool.com)
- [Documentation](https://docs.multi-upload-tool.com)

## License

MIT
