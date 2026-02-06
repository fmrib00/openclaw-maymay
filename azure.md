# Azure 基础设施配置

> 最后更新：2026-02-06 12:40
> 维护者：Yongyue
> 来源：maymay-backend 代码分析

---

## Connection String

```
DefaultEndpointsProtocol=https;AccountName=<ACCOUNT_NAME>;AccountKey=<ACCOUNT_KEY>;EndpointSuffix=core.windows.net
```

**Account Name:** maymaynail

**⚠️ 注意:** 完整的connection string包含敏感信息，请从环境变量或安全配置文件中读取，不要直接写在代码或文档中。

**用途:** Maymay穿戴甲平台的 Azure Storage
- **Blob 存储** - 图片、文件上传
- **Table 存储** - 业务数据（商品、用户、订单等）

---

## 重要表格 (Tables) 详细结构

### 1️⃣ maymayproducts - 商品表

**用途:** 存储穿戴甲商品的所有信息

**表结构:**
- **PartitionKey:** `"Nail"` (固定值)
- **RowKey:** 商品ID (如 `"M30046"`, `"XS10010"`, 或 `"prod_abc123"`)

**字段列表:**

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `id` | string | ✅ | 商品ID（同RowKey） |
| **简体中文** | | | |
| `name` | string | ✅ | 商品名称（简体中文） |
| `summary` | string | ✅ | 商品简介（简体中文） |
| `styles` | string (JSON) | ✅ | 风格标签数组（JSON字符串，如 `["红色","亮片"]`） |
| **英文** | | | |
| `name_en` | string | | 商品名称（英文） |
| `summary_en` | string | | 商品简介（英文） |
| `styles_en` | string (JSON) | | 风格标签数组（英文，JSON） |
| **繁体中文** | | | |
| `name_tw` | string | | 商品名称（繁体中文） |
| `summary_tw` | string | | 商品简介（繁体中文） |
| `styles_tw` | string (JSON) | | 风格标签数组（繁体中文，JSON） |
| **通用字段** | | | |
| `price` | float | ✅ | 价格 |
| `size` | string | ✅ | 尺寸：`"XS"`, `"S"`, `"M"`, `"L"` |
| `image_url` | string | | 图片URL |
| `stock` | int | ✅ | 库存数量 |
| `status` | string | ✅ | 状态：`"active"` (在售), `"inactive"` (下架), `"tracking"` (监控中) |
| `product_code` | string | | 商品代码 |
| `created_at` | datetime (ISO) | ✅ | 创建时间（Asia/Taipei时区） |
| `updated_at` | datetime (ISO) | ✅ | 更新时间（Asia/Taipei时区） |

**注意:**
- `styles` 字段存储为 JSON 字符串数组，读写时需要序列化/反序列化
- 库存不足时无法下单
- 只有 `status="active"` 的商品可以购买

---

### 2️⃣ maymayusers - 用户表

**用途:** 存储用户信息（买家和管理员）

**表结构:**
- **PartitionKey:** 用户邮箱
- **RowKey:** `"0"` (固定值)

**字段列表:**

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `id` | string | ✅ | 用户ID（即邮箱） |
| `email` | string (Email) | ✅ | 邮箱 |
| `name` | string | | 用户姓名 |
| `image` | string | | 头像URL |
| `password` | string | | 密码（bcrypt哈希，Google用户为空） |
| `google_sub` | string | | Google唯一标识符（OAuth登录用户） |
| `user_type` | string | ✅ | 用户类型：`"buyer"` (买家), `"admin"` (管理员) |
| `age` | int | ✅ | 年龄（1-150） |
| `gender` | string | ✅ | 性别：`"male"`, `"female"`, `"other"` |
| `preferred_language` | string | | 首选语言：`"en"`, `"zh-CN"`, `"zh-TW"`（默认 `"zh-TW"`） |
| `address` | string | | 收货地址 |
| `created_at` | datetime (ISO) | ✅ | 创建时间 |
| `updated_at` | datetime (ISO) | ✅ | 更新时间 |

**注意:**
- 密码使用 bcrypt 哈希存储
- Google OAuth 用户没有密码，使用 `google_sub` 标识
- `user_type="admin"` 的用户可以访问后台管理功能

---

### 3️⃣ maymayorders - 订单表

**用途:** 存储订单信息

**表结构:**
- **PartitionKey:** 订单ID
- **RowKey:** 订单ID（同PartitionKey）

**字段列表:**

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `id` | string | ✅ | 订单ID（如 `"ORD_20260206_ABC12345"`） |
| `user_email` | string (Email) | ✅ | 买家邮箱 |
| `status` | string | ✅ | 订单状态：`"pending"`, `"confirmed"`, `"processing"`, `"shipped"`, `"delivered"`, `"cancelled"` |
| `items` | string (JSON) | ✅ | 订单商品数组（JSON字符串） |
| `subtotal` | float | ✅ | 小计 |
| `total` | float | ✅ | 总计 |
| `shipping_address` | string | ✅ | 收货地址 |
| `shipping_name` | string | ✅ | 收货人姓名 |
| `shipping_phone` | string | | 收货人电话 |
| `notes` | string | | 订单备注 |
| `locale` | string | | 客户语言（用于邮件通知） |
| `created_at` | datetime (ISO) | ✅ | 创建时间 |
| `updated_at` | datetime (ISO) | ✅ | 更新时间 |
| `payment_notified_at` | datetime (ISO) | | 买家通知付款时间（QR码流程） |

**items 字段结构（JSON数组）:**
```json
[
  {
    "product_id": "M30046",
    "product_name": "红色美甲",
    "product_code": "M30046",
    "product_image_url": "https://...",
    "quantity": 2,
    "price": 299.0,
    "subtotal": 598.0
  }
]
```

**订单状态流程:**
1. `pending` - 待确认
2. `confirmed` - 已确认
3. `processing` - 处理中
4. `shipped` - 已发货
5. `delivered` - 已送达
6. `cancelled` - 已取消

---

### 4️⃣ maymaypayments - 支付记录表

**用途:** 存储支付记录

**表结构:**
- **PartitionKey:** 年-月（`"YYYY-MM"`，如 `"2026-02"`）
- **RowKey:** 支付ID（如 `"PAY_20260206_ABC12345"`）

**字段列表:**

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `id` | string | ✅ | 支付ID |
| `order_id` | string | ✅ | 关联的订单ID |
| `payment_method` | string | ✅ | 支付方式：`"line_pay"`, `"wechat_pay"`, `"alipay"`, `"credit_card"` |
| `amount` | float | ✅ | 支付金额 |
| `currency` | string | ✅ | 货币代码（默认 `"TWD"`） |
| `status` | string | ✅ | 支付状态：`"pending"`, `"processing"`, `"success"`, `"failed"`, `"cancelled"`, `"refunded"` |
| `transaction_id` | string | | 支付网关交易ID |
| `line_pay_transaction_id` | string | | LINE Pay交易ID |
| `payment_url` | string | | 支付URL（用于跳转到支付页面） |
| `created_at` | datetime (ISO) | ✅ | 创建时间 |
| `updated_at` | datetime (ISO) | ✅ | 更新时间 |
| `paid_at` | datetime (ISO) | | 支付完成时间 |

**支付状态流程:**
1. `pending` - 待支付
2. `processing` - 处理中
3. `success` - 支付成功
4. `failed` - 支付失败
5. `cancelled` - 已取消
6. `refunded` - 已退款

---

### 5️⃣ maymayFavorites - 用户收藏表

**用途:** 存储用户收藏的商品

**表结构:**
- **PartitionKey:** 用户邮箱
- **RowKey:** 商品ID

**字段列表:**

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `product_id` | string | ✅ | 商品ID |
| `created_at` | datetime (ISO) | ✅ | 收藏时间 |

**注意:**
- 复合主键：`(user_email, product_id)` 确保唯一性
- 用于查询用户收藏的所有商品

---

### 6️⃣ maymayCommonStyles - 常用样式表

**用途:** 存储商品风格标签（多语言）

**表结构:**
- **PartitionKey:** `"CommonStyle"` (固定值)
- **RowKey:** 样式ID（如 `"style_abc123"`）

**字段列表:**

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `id` | string | ✅ | 样式ID（同RowKey） |
| `name_zh_cn` | string | ✅ | 样式名称（简体中文） |
| `name_en` | string | ✅ | 样式名称（英文） |
| `name_zh_tw` | string | ✅ | 样式名称（繁体中文） |
| `created_at` | datetime (ISO) | ✅ | 创建时间 |

**默认样式（24个）:**
- 颜色：red, pink, rose, orange, yellow, green, blue, purple
- 质感：glitter, sparkle, matte, glossy, shimmer
- 场合：party, wedding, casual, office, summer, winter
- 图案：floral, geometric, striped, dotted, abstract

---

### 7️⃣ BlackListIP - IP黑名单表

**用途:** 存储被屏蔽的IP地址

**表结构:**
- **PartitionKey:** IP地址
- **RowKey:** IP地址（同PartitionKey）

**字段列表:**

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `reason` | string | | 屏蔽原因 |
| `created_at` | datetime (ISO) | | 屏蔽时间 |
| `PartitionKey` | string | ✅ | IP地址 |
| `RowKey` | string | ✅ | IP地址 |

**注意:**
- 用于API访问控制
- 在内存中缓存以快速检查

---

## 表操作规则

### 🔴 重要原则

1. **严格遵守数据类型:** 不要试图用自己的方式更改数据或数据类型
2. **失败处理:** 如果操作失败，不做任何更改
3. **JSON字段:** `styles`, `items` 等字段存储为JSON字符串，需要序列化/反序列化
4. **时间格式:** 所有时间使用 ISO 8601 格式，时区为 Asia/Taipei

### 📋 常用操作

**创建实体:**
```python
entity = {
    "PartitionKey": "...",
    "RowKey": "...",
    "field": "value"
}
table_client.create_entity(entity=entity)
```

**查询实体:**
```python
entities = table_client.query_entities(
    query_filter="PartitionKey eq 'value'"
)
```

**更新实体:**
```python
table_client.update_entity(entity=updated_entity)
```

**删除实体:**
```python
table_client.delete_entity(partition_key="...", row_key="...")
```

---

## 服务层代码位置

- **产品服务:** `/home/yongyue/maymay-backend/app/services/product_service.py`
- **用户服务:** `/home/yongyue/maymay-backend/app/services/auth_service.py`
- **订单服务:** `/home/yongyue/maymay-backend/app/services/order_service.py`
- **支付服务:** `/home/yongyue/maymay-backend/app/services/payment_service.py`
- **收藏服务:** `/home/yongyue/maymay-backend/app/services/favorites_service.py`
- **样式服务:** `/home/yongyue/maymay-backend/app/services/common_style_service.py`
- **IP黑名单:** `/home/yongyue/maymay-backend/app/services/blacklist_ip_service.py`

---

## 模型定义位置

- **Product:** `/home/yongyue/maymay-backend/app/models/product.py`
- **User:** `/home/yongyue/maymay-backend/app/models/user.py`
- **Order:** `/home/yongyue/maymay-backend/app/models/order.py`
- **Payment:** `/home/yongyue/maymay-backend/app/models/payment.py`
- **CommonStyle:** `/home/yongyue/maymay-backend/app/models/common_style.py`

---

## 缓存策略

系统使用 Redis 缓存常用查询结果：
- **用户缓存:** `user:{email}`, `user:google_sub:{sub}` (TTL: 1小时)
- **产品缓存:** `product:{id}` (TTL: 1小时)
- **样式缓存:** `common_styles:all`, `common_styles:lang:{lang}` (TTL: 1小时)
- **支付缓存:** `payment:{id}`, `payment:order:{order_id}` (TTL: 1小时)

---

*此文档基于 maymay-backend 代码自动生成，最后更新于 2026-02-06*
