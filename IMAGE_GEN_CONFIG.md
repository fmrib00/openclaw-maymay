# 图像生成全局配置

## 默认设置

```yaml
provider: doubao        # 默认使用豆包图像生成
quality: 2k            # 默认质量2K
aspect_ratio: 3:4      # 默认宽高比（竖版，适合漫画）
model: doubao-seedream-4-5-251128  # 默认豆包模型
```

## 配置说明

### Provider（提供商）
- `doubao`: 豆包图像生成（推荐，性价比高）✅ 已集成
- `google`: Google Gemini
- `openai`: OpenAI DALL-E
- `dashscope`: 阿里云通义万象

### Quality（质量）
- `2k`: 高质量（2048px，默认）
- `normal`: 标准质量（1024px，速度快）

### Aspect Ratio（宽高比）
- `3:4`: 竖版（适合漫画页面，默认）
- `4:3`: 横版
- `1:1`: 方形
- `16:9`: 宽屏

## 豆包模型选项

```yaml
# 推荐（默认）
doubao-seedream-4-5-251128  # 豆包Seedream 4.5

# 备选
doubao-seedream-4-0-250828  # 豆包4.0模型
```

## API配置

豆包API密钥已配置在 `~/.baoyu-skills/.env`：

```bash
DOUBAO_API_KEY=e739fdca-4dd0-452c-ab93-5ecb096f7e82
DOUBAO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
DOUBAO_IMAGE_MODEL=doubao-seedream-4-5-251128
```

## 使用示例

```bash
# 使用全局默认设置（豆包+2K+3:4）
bun main.ts -p "A cat" --image cat.png

# 指定宽高比
bun main.ts -p "A cat" --image cat.png --ar 16:9

# 覆盖默认设置
bun main.ts -p "A cat" --image cat.png --provider openai --quality normal
```

## 测试结果

✅ **豆包图像生成已成功集成并测试！**

- 测试图片：2048x2731, 1.1MB
- 生成速度：约5-10秒
- 质量优秀

## 重要提醒

所有需要生成图片的功能都必须使用此配置作为默认设置！
