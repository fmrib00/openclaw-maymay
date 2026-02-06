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

## Azure Storage Configuration

**详细配置文件:** `/home/yongyue/.openclaw/workspace/azure.md`

**Connection String:** `credentials/azure-storage.txt` (敏感信息，已加入 .gitignore)

**Account Name:** maymaynail

**用途:** Maymay穿戴甲平台的Azure Storage
- Blob存储（图片、文件上传等）
- Table存储（商品、用户、订单等数据）

**核心表格:**
- maymayproducts - 商品清单
- maymayusers - 用户清单
- maymayorders - 订单清单
- maymaypayments - 付款清单
- maymayFavorites - 用户收藏
- maymayCommonStyles - 常用样式
- BlackListIP - IP黑名单

**重要提醒:** 当需要读取/添加/修改表内容时，严格遵守用户给出的规则，不要试图用自己的方式更改数据或数据类型
