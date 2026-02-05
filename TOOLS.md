# TOOLS.md - 工具备忘录

## Telegram文件发送方法

当需要通过message工具发送文件到Telegram时，使用以下curl命令：

```bash
curl -X POST "https://api.telegram.org/bot<botToken>/sendDocument" \
  -H "Content-Type: multipart/form-data" \
  -F "chat_id=<chatId>" \
  -F "document=@<文件路径>" 2>&1
```

**说明：**
- `botToken`: 从 `/home/yongyue/.openclaw/openclaw.json` 读取 `channels.telegram.botToken`
- `chatId`: 目标聊天ID（如 `8310450673`）
- `document=@路径`: 使用 `@` 符号上传文件

这个方法适用于发送文件附件，比message工具的path参数更可靠。
