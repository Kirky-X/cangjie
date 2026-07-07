# [产品/系统名称（英文名）] - API 文档

> **文档状态：** 🟡 评审中 / 🟢 已通过 / 🔴 驳回
>
> **保密级别：** 机密 / 内部公开 / 公开
>
> **版本：** v1.0.0
>
> **日期：** YYYY-MM-DD
>
> **撰写人：** [后端负责人 / API Owner]
>
> **评审人：** [前端负责人 / 架构师]
>
> **阅读对象：** 前端工程师、后端工程师、测试工程师、第三方接入方、SDK 维护者
>
> **关联 TRD：** [TRD编号/文件名]
>
> **关联架构文档：** [ADD编号/文件名]
>
> **OpenAPI Spec：** [openapi.yaml 路径或 URL]

---

## 0. 文档导读

### 0.1 文档目的与适用范围

**API 文档回答**："端点长什么样、怎么调、返回什么、出错怎么办"——前后端、第三方与 SDK 维护者的契约层。

**适用场景：**

- ✅ 对外开放的 REST / GraphQL / gRPC 接口契约
- ✅ 前后端分离架构下的接口联调依据
- ✅ 第三方接入、SDK 自动生成（基于 OpenAPI 3.x）
- ✅ API 网关、Mock 服务、契约测试的单一事实源
- ❌ 内部函数签名（用代码注释 / TSDoc / rustdoc）
- ❌ 数据库表结构（用 DB 设计文档）

### 0.2 相关文档

| 文档类型 | 文件名              | 相关章节   |
| :------- | :------------------ | :--------- |
| [类型]   | [文件名] [行号范围] | [章节描述] |

> **引用格式说明**：关联文档使用 `文件名 行号范围` 格式（如 `【模板】技术需求文档(TRD).md 3-17`），行号随文档更新可能变化，请以实际内容为准。

### 0.3 变更记录

| 版本   | 日期       | 修订人 | 变更内容                                                                 | 审核人   |
| :----- | :--------- | :----- | :----------------------------------------------------------------------- | :------- |
| v0.1   | YYYY-MM-DD | [姓名] | 初稿：核心端点列表 + 认证方式                                             | [姓名]   |
| v0.2   | YYYY-MM-DD | [姓名] | 补充错误码字典 + 限流策略                                                 | [姓名]   |
| v1.0   | YYYY-MM-DD | [姓名] | 正式发布，对齐 OpenAPI 3.1                                                | [架构师] |
| v1.0.1 | YYYY-MM-DD | [姓名] | 修正 `/v1/users/{id}` 响应字段 `deleted_at` 可空性标注                    | —        |

---

## 1. 概述（Overview）

> **5 秒说清：** 这是一套什么 API、给谁用、解决什么问题。

| 要素             | 内容                                                              |
| :--------------- | :---------------------------------------------------------------- |
| **API 名称**     | [如：用户中心 OpenAPI]                                            |
| **API 定位**     | [如：面向移动端 / Web / 第三方 ISV 的统一用户资产查询与变更接口] |
| **协议**         | HTTPS / RESTful / GraphQL / gRPC                                  |
| **基础 URL**     | `https://{env}.example.com/api/v{version}`                        |
| **环境**         | 线上：`api.example.com` / 预发：`api-pre.example.com` / 沙箱：`sandbox.example.com` |
| **当前版本**     | v1                                                                |
| **OpenAPI 版本** | OpenAPI 3.1.0                                                     |
| **MIME 类型**    | `application/json; charset=utf-8`                                 |
| **字符集**       | UTF-8                                                             |
| **时区**         | 所有时间戳使用 ISO 8601 UTC（如 `2026-07-05T08:00:00Z`）          |

---

## 2. 认证与授权（Authentication & Authorization）

### 2.1 认证方式

| 方式             | 适用场景               | 凭证位置                                  | 凭证有效期       |
| :--------------- | :--------------------- | :---------------------------------------- | :--------------- |
| **Bearer Token** | 用户态 API             | `Authorization: Bearer {access_token}`   | 2 小时，可刷新   |
| **API Key**      | 服务端到服务端         | `X-API-Key: {api_key}`                    | 长期，可吊销     |
| **OAuth 2.1**    | 第三方接入             | `Authorization: Bearer {oauth_token}`    | 由授权流程决定   |
| **mTLS**         | 金融级 / 内网敏感链路  | 客户端证书                                | 由证书生命周期决定 |

### 2.2 获取 Token

```http
POST /v1/auth/token HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "client_id": "{client_id}",
  "client_secret": "{client_secret}"
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access_token": "{token}",
  "token_type": "Bearer",
  "expires_in": 7200,
  "refresh_token": "{refresh_token}"
}
```

### 2.3 权限模型（Scope）

| Scope            | 描述                 | 适用端点                       |
| :--------------- | :------------------- | :----------------------------- |
| `user:read`      | 读取用户基础信息     | `GET /v1/users/*`              |
| `user:write`     | 修改用户信息         | `POST/PUT/PATCH /v1/users/*`   |
| `order:read`     | 读取订单             | `GET /v1/orders/*`             |
| `order:write`    | 创建/取消订单        | `POST /v1/orders`              |
| `admin:*`        | 管理后台全权         | 仅内网管理端                   |

### 2.4 鉴权失败响应

| HTTP 状态码 | error_code            | 说明                  |
| :---------: | :-------------------- | :-------------------- |
| 401         | `UNAUTHENTICATED`     | 缺少凭证 / Token 失效 |
| 403         | `PERMISSION_DENIED`   | Scope 不足            |
| 403         | `TOKEN_REVOKED`       | Token 已被吊销        |

---

## 3. 通用约定（Conventions）

### 3.1 请求格式

- **Content-Type**：`application/json; charset=utf-8`（除文件上传用 `multipart/form-data`）
- **Accept**：`application/json`
- **必填请求头**：

| Header              | 说明                            | 示例                          |
| :------------------ | :------------------------------ | :---------------------------- |
| `Authorization`     | Bearer Token / API Key          | `Bearer eyJhbGciOi...`        |
| `X-Request-Id`      | 请求追踪 ID（缺省由网关生成）   | `req_8f14e45f-ceea-...`       |
| `X-Timestamp`       | 客户端时间戳（防重放）          | `1752835200`                  |
| `X-Signature`       | 请求签名（敏感接口必填）        | `HMAC-SHA256` 输出            |
| `User-Agent`        | 客户端标识                       | `MyApp/1.0 (iOS 17)`          |

### 3.2 响应格式（统一信封）

**成功响应：**

```json
{
  "code": 0,
  "message": "ok",
  "data": { },
  "request_id": "req_8f14e45f-ceea-467f-a830-...",
  "timestamp": "2026-07-05T08:00:00Z"
}
```

**错误响应：**

```json
{
  "code": 40001,
  "message": "参数校验失败",
  "errors": [
    { "field": "email", "issue": "格式不合法" }
  ],
  "request_id": "req_8f14e45f-ceea-467f-a830-...",
  "timestamp": "2026-07-05T08:00:00Z"
}
```

| 字段          | 类型     | 说明                                          |
| :------------ | :------- | :-------------------------------------------- |
| `code`        | integer  | 0 表示成功，非 0 表示业务错误码                |
| `message`     | string   | 面向人类的简短描述                             |
| `data`        | object   | 业务数据，错误时缺省                           |
| `errors`      | array    | 字段级错误明细，仅校验失败时返回               |
| `request_id`  | string   | 全链路追踪 ID，排查问题必提供                  |
| `timestamp`   | string   | 服务端响应时间，ISO 8601 UTC                   |

### 3.3 分页约定

- **方式**：游标分页（推荐）/ 偏移分页（兼容）
- **请求参数**：

| 参数        | 类型    | 默认 | 说明                                   |
| :---------- | :------ | :--- | :------------------------------------- |
| `page_size` | integer | 20   | 每页数量，上限 100                     |
| `cursor`    | string  | —    | 游标，首次请求不传，后续从响应取回     |
| `page`      | integer | 1    | 偏移分页时使用，与 cursor 互斥         |

- **响应字段**：

```json
{
  "data": {
    "items": [ ],
    "page_info": {
      "has_next": true,
      "next_cursor": "eyJpZCI6MTIzNDV9",
      "total": 1024
    }
  }
}
```

### 3.4 命名与类型约定

| 维度         | 约定                                                   | 示例                          |
| :----------- | :----------------------------------------------------- | :---------------------------- |
| 字段命名     | `snake_case`                                           | `user_id` / `created_at`      |
| 时间格式     | ISO 8601 UTC 字符串                                    | `2026-07-05T08:00:00Z`        |
| 金额         | 整数 + 字符串（最小货币单位，避免浮点误差）            | `"199"` 表示 ¥1.99            |
| 布尔         | `true` / `false`                                       | 不使用 0/1 替代               |
| 枚举         | 小写蛇形                                                | `order_status: "paid"`        |
| ID 类型      | 字符串（避免 JSON 数字精度丢失）                        | `"id": "1234567890123456789"` |
| 空值         | `null` 而非省略字段                                     | 保持字段可空性显式             |
| 金额符号     | `$` 在飞书 / Markdown 中需转义为 `\$`                   | `\$0.05`                      |

### 3.5 HTTP 方法语义

| 方法     | 语义         | 幂等性 | 安全性 | 示例                       |
| :------- | :----------- | :----: | :----: | :------------------------- |
| `GET`    | 查询         |   ✅   |   ✅   | `GET /v1/users/123`        |
| `POST`   | 创建 / 动作  |   ❌   |   ❌   | `POST /v1/users`           |
| `PUT`    | 全量替换     |   ✅   |   ❌   | `PUT /v1/users/123`        |
| `PATCH`  | 部分更新     |   ❌   |   ❌   | `PATCH /v1/users/123`      |
| `DELETE` | 删除         |   ✅   |   ❌   | `DELETE /v1/users/123`     |

### 3.6 幂等性

- **写操作幂等**：客户端在 `Idempotency-Key` 头中传入 UUID，服务端 24 小时内对相同 key 返回首次结果
- **适用范围**：所有 `POST` / `PUT` / `PATCH` / `DELETE`
- **示例**：`Idempotency-Key: 8f14e45f-ceea-467f-a830-a0d4e8d6c5b1`

---

## 4. 端点列表（Endpoint Index）

> **说明**：所有端点详述见 §5；本表为快速索引。

| #   | 方法     | 路径                           | 名称           | Scope          | 备注           |
| :-: | :------- | :----------------------------- | :------------- | :------------- | :------------- |
| 1   | `POST`   | `/v1/auth/token`               | 获取 Token     | —              | 公开端点       |
| 2   | `POST`   | `/v1/auth/token:refresh`       | 刷新 Token     | —              | 需要 refresh_token |
| 3   | `GET`    | `/v1/users/{user_id}`          | 查询用户       | `user:read`    |                |
| 4   | `POST`   | `/v1/users`                    | 创建用户       | `user:write`   |                |
| 5   | `PATCH`  | `/v1/users/{user_id}`          | 更新用户       | `user:write`   | 部分更新       |
| 6   | `DELETE` | `/v1/users/{user_id}`          | 删除用户       | `user:write`   | 软删除         |
| 7   | `GET`    | `/v1/users`                    | 用户列表       | `user:read`    | 分页           |
| 8   | `GET`    | `/v1/orders/{order_id}`        | 查询订单       | `order:read`   |                |
| 9   | `POST`   | `/v1/orders`                   | 创建订单       | `order:write`  | 幂等必填       |
| 10  | `POST`   | `/v1/orders/{order_id}:cancel` | 取消订单       | `order:write`  |                |

---

## 5. 端点详述（Endpoint Reference）

### 5.1 获取 Token

`POST /v1/auth/token`

**描述**：使用客户端凭证换取访问 Token。

**请求参数**

| 位置     | 字段            | 类型    | 必填 | 说明                |
| :------- | :-------------- | :------ | :--: | :------------------ |
| body     | `grant_type`    | string  |  ✅  | `client_credentials` / `refresh_token` |
| body     | `client_id`     | string  |  ✅  | 客户端 ID           |
| body     | `client_secret` | string  |  ✅  | 客户端密钥          |
| body     | `refresh_token` | string  |  —  | grant_type=refresh_token 时必填 |

**请求示例**

```bash
curl -X POST https://api.example.com/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "{client_id}",
    "client_secret": "{client_secret}"
  }'
```

**成功响应** `200 OK`

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 7200,
    "refresh_token": "rft_8f14e45fceea467f..."
  },
  "request_id": "req_8f14e45f-ceea-467f-a830-a0d4e8d6c5b1",
  "timestamp": "2026-07-05T08:00:00Z"
}
```

**错误响应**

| HTTP | code   | message          |
| ---: | :----- | :--------------- |
| 400  | 40001  | 参数校验失败     |
| 401  | 40101  | client_id 不存在 |
| 401  | 40102  | client_secret 错误 |

---

### 5.2 查询用户

`GET /v1/users/{user_id}`

**描述**：根据用户 ID 查询用户详情。

**路径参数**

| 字段       | 类型   | 必填 | 说明              |
| :--------- | :----- | :--: | :---------------- |
| `user_id`  | string |  ✅  | 用户唯一标识      |

**查询参数**

| 字段       | 类型    | 必填 | 说明                          |
| :--------- | :------ | :--: | :---------------------------- |
| `fields`   | string  |  —  | 返回字段筛选，逗号分隔        |

**请求示例**

```bash
curl -X GET https://api.example.com/v1/users/123 \
  -H "Authorization: Bearer {access_token}"
```

**成功响应** `200 OK`

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "user_id": "123",
    "nickname": "张三",
    "email": "zhangsan@example.com",
    "phone": "138****0000",
    "avatar_url": "https://cdn.example.com/avatar/123.png",
    "status": "active",
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-07-05T08:00:00Z"
  },
  "request_id": "req_8f14e45f-ceea-467f-a830-a0d4e8d6c5b1",
  "timestamp": "2026-07-05T08:00:00Z"
}
```

**错误响应**

| HTTP | code   | message          |
| ---: | :----- | :--------------- |
| 401  | 40100  | 未认证           |
| 403  | 40300  | Scope 不足       |
| 404  | 40400  | 用户不存在       |

---

### 5.3 创建用户

`POST /v1/users`

**描述**：创建一个新用户。

**请求体**

| 字段        | 类型    | 必填 | 校验规则                       | 说明         |
| :---------- | :------ | :--: | :----------------------------- | :----------- |
| `nickname`  | string  |  ✅  | 1-32 字符，不含敏感词          | 昵称         |
| `email`     | string  |  ✅  | RFC 5322 邮箱格式              | 邮箱         |
| `phone`     | string  |  —  | E.164 格式 `+8613800000000`    | 手机号       |
| `password`  | string  |  ✅  | ≥ 8 位，含大小写 + 数字         | 密码（明文传入，服务端 bcrypt）|

**请求示例**

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer {access_token}" \
  -H "Idempotency-Key: 8f14e45f-ceea-467f-a830-a0d4e8d6c5b1" \
  -H "Content-Type: application/json" \
  -d '{
    "nickname": "张三",
    "email": "zhangsan@example.com",
    "password": "********"
  }'
```

**成功响应** `201 Created`

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "user_id": "124",
    "nickname": "张三",
    "email": "zhangsan@example.com",
    "status": "active",
    "created_at": "2026-07-05T08:00:00Z"
  },
  "request_id": "req_8f14e45f-ceea-467f-a830-a0d4e8d6c5b1",
  "timestamp": "2026-07-05T08:00:00Z"
}
```

**错误响应**

| HTTP | code   | message              |
| ---: | :----- | :------------------- |
| 400  | 40001  | 参数校验失败         |
| 409  | 40901  | 邮箱已注册           |

---

> **端点续写说明**：后续端点（5.4 ~ 5.10）按上述结构补充：路径参数 / 查询参数 / 请求体 / 请求示例 / 成功响应 / 错误响应。结构保持完全一致，避免风格漂移。

---

## 6. 数据模型（Schemas）

> **说明**：本节定义所有端点共享的数据模型，与 OpenAPI `components.schemas` 一一对应。

### 6.1 User

| 字段          | 类型      | 必填 | 可空 | 说明                          |
| :------------ | :-------- | :--: | :--: | :---------------------------- |
| `user_id`     | string    |  ✅  |  —   | 用户唯一 ID                   |
| `nickname`    | string    |  ✅  |  —   | 昵称                          |
| `email`       | string    |  ✅  |  —   | 邮箱                          |
| `phone`       | string    |  —   |  ✅  | 手机号（E.164）               |
| `avatar_url`  | string    |  —   |  ✅  | 头像 URL                      |
| `status`      | enum      |  ✅  |  —   | `active` / `inactive` / `banned` |
| `created_at`  | datetime  |  ✅  |  —   | 创建时间（ISO 8601 UTC）      |
| `updated_at`  | datetime  |  ✅  |  —   | 更新时间（ISO 8601 UTC）      |
| `deleted_at`  | datetime  |  —   |  ✅  | 软删除时间，未删除为 null     |

### 6.2 Order

| 字段            | 类型      | 必填 | 可空 | 说明                          |
| :-------------- | :-------- | :--: | :--: | :---------------------------- |
| `order_id`      | string    |  ✅  |  —   | 订单 ID                       |
| `user_id`       | string    |  ✅  |  —   | 下单用户 ID                   |
| `amount`        | string    |  ✅  |  —   | 金额（最小货币单位，字符串）  |
| `currency`      | string    |  ✅  |  —   | ISO 4217 货币码（如 `CNY`）   |
| `order_status`  | enum      |  ✅  |  —   | `pending` / `paid` / `shipped` / `cancelled` / `refunded` |
| `items`         | array     |  ✅  |  —   | 商品列表                      |
| `created_at`    | datetime  |  ✅  |  —   | 下单时间                      |
| `paid_at`       | datetime  |  —   |  ✅  | 支付时间                      |

### 6.3 Pagination

| 字段          | 类型     | 必填 | 说明                            |
| :------------ | :------- | :--: | :------------------------------ |
| `items`       | array    |  ✅  | 当前页数据                      |
| `page_info`   | object   |  ✅  | 分页信息                        |
| `page_info.has_next`   | boolean | ✅ | 是否有下一页                    |
| `page_info.next_cursor`| string  | — | 下一页游标                      |
| `page_info.total`      | integer | — | 总条数（偏移分页时返回）        |

---

## 7. 错误码字典（Error Codes）

### 7.1 错误码结构

错误码为 5 位整数，分段如下：

| 段位      | 含义                     | 示例                |
| :-------- | :----------------------- | :------------------ |
| 第 1 位   | HTTP 状态码缩写          | `4` = 4xx，`5` = 5xx |
| 第 2-3 位 | 模块编号                 | `00` = 通用，`01` = 认证，`02` = 用户 |
| 第 4-5 位 | 模块内错误序号           | `01` = 第 1 个错误   |

### 7.2 通用错误码

| HTTP | code   | message              | 说明                          |
| ---: | :----- | :------------------- | :---------------------------- |
| 400  | 40000  | 请求格式错误         | JSON 解析失败 / 缺少必填头    |
| 400  | 40001  | 参数校验失败         | 字段级错误见 `errors`         |
| 401  | 40100  | 未认证               | 缺少 / 失效的 Token           |
| 403  | 40300  | 权限不足             | Scope 不匹配                  |
| 404  | 40400  | 资源不存在           |                               |
| 409  | 40900  | 资源冲突             | 唯一性冲突                    |
| 422  | 42200  | 业务校验失败         | 业务规则不允许                |
| 429  | 42900  | 请求过多             | 触发限流                      |
| 500  | 50000  | 服务内部错误         | 联系运维，提供 request_id     |
| 502  | 50200  | 网关错误             | 上游不可达                    |
| 503  | 50300  | 服务不可用           | 维护中 / 过载                 |
| 504  | 50400  | 网关超时             |                               |

### 7.3 业务错误码

| HTTP | code   | message              | 模块     |
| ---: | :----- | :------------------- | :------- |
| 401  | 40101  | client_id 不存在     | 认证     |
| 401  | 40102  | client_secret 错误   | 认证     |
| 409  | 40901  | 邮箱已注册           | 用户     |
| 409  | 40902  | 手机号已绑定         | 用户     |
| 422  | 42201  | 订单不可取消         | 订单     |
| 422  | 42202  | 库存不足             | 订单     |

---

## 8. 版本管理（Versioning）

### 8.1 版本策略

- **版本位置**：URL 路径前缀（`/v1/`、`/v2/`）
- **兼容性承诺**：
  - 同一大版本内：新增字段 / 新增端点 / 放宽校验 → 向后兼容，不破坏客户端
  - 删除字段 / 改变字段类型 / 收紧校验 / 删除端点 → 必须升大版本
- **支持周期**：旧大版本在新版本发布后维护 ≥ 12 个月，到期前 90 天公告废弃

### 8.2 废弃流程

```mermaid
flowchart LR
    A[新版发布] --> B[旧版标记 Deprecated]
    B --> C[响应头返回 Sunset: date]
    C --> D[90 天公告期]
    D --> E[下线旧版]
    style A fill:#c8e6c9
    style E fill:#ffcdd2
```

- **响应头标注**：`Deprecation: true` + `Sunset: Wed, 5 Oct 2026 00:00:00 GMT`
- **公告渠道**：开发者邮件 + API 文档首页 + 响应头三重告知

### 8.3 变更分类

| 变更类型           | 是否兼容 | 是否需升版本 | 示例                                |
| :----------------- | :------: | :----------: | :---------------------------------- |
| 新增可选请求字段   |   ✅     |     ❌       | 增加 `fields` 查询参数              |
| 新增响应字段       |   ✅     |     ❌       | User 增加 `avatar_url`              |
| 删除字段           |   ❌     |     ✅       | 移除 `phone`                        |
| 改变字段类型       |   ❌     |     ✅       | `amount` 从 number 改为 string      |
| 收紧校验规则       |   ❌     |     ✅       | `password` 最小长度 6 → 8           |
| 改变错误码语义     |   ❌     |     ✅       | 40101 从"client_id 错误"改为"Token 失效" |

---

## 9. 安全与限流（Security & Rate Limiting）

### 9.1 限流策略

| 维度         | 限制                 | 触发后行为                | Header 提示                          |
| :----------- | :------------------- | :------------------------ | :----------------------------------- |
| 单 Token      | 600 次 / 分钟        | 429 + `Retry-After`       | `X-RateLimit-Remaining`              |
| 单 IP         | 1200 次 / 分钟       | 429                       | `X-RateLimit-Limit`                  |
| 单应用        | 100 万次 / 天        | 429 + 告警                | `X-RateLimit-Reset`                  |
| 写操作        | 60 次 / 分钟         | 429                       | —                                    |

**429 响应示例：**

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 30
X-RateLimit-Limit: 600
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1752835230

{
  "code": 42900,
  "message": "请求过多，请稍后再试",
  "request_id": "req_8f14e45f-ceea-467f-a830-a0d4e8d6c5b1",
  "timestamp": "2026-07-05T08:00:00Z"
}
```

### 9.2 配额管理

| 配额项       | 默认值       | 升级路径                       |
| :----------- | :----------- | :----------------------------- |
| 日调用量     | 100 万次     | 申请企业版配额                 |
| 并发连接     | 100          | 联系商务                       |
| 历史数据查询 | 30 天        | 升级数据留存套餐               |

### 9.3 安全最佳实践

- **传输加密**：强制 TLS 1.3，禁用旧版本
- **请求签名**：敏感接口（支付、退款、删除）强制 `X-Signature`
- **防重放**：`X-Timestamp` 偏差 ±5 分钟外拒绝；nonce 5 分钟内不可重复
- **密钥存储**：客户端密钥不可硬编码，使用 KMS / 环境变量
- **审计日志**：所有写操作、敏感读操作记录 ≥ 1 年
- **PII 脱敏**：响应中手机号、身份证、邮箱默认脱敏，需明文时申请 `pii:read` scope

---

## 10. 附录（Appendix）

### 10.1 SDK 与工具

| 语言     | 仓库                                | 自动生成方式       |
| :------- | :---------------------------------- | :----------------- |
| Java     | `github.com/example/sdk-java`       | OpenAPI Generator  |
| Python   | `github.com/example/sdk-python`     | openapi-python-client |
| Node.js  | `github.com/example/sdk-node`       | openapi-typescript |
| Go       | `github.com/example/sdk-go`         | oapi-codegen       |

### 10.2 Mock 与契约测试

- **Mock 服务**：基于 OpenAPI 自动生成，URL `https://mock.example.com`
- **契约测试**：Pact / Dredd，CI 中校验实现与文档一致
- **Postman Collection**：`postman/api-collection.json`

### 10.3 术语表

| 术语        | 英文              | 释义                          |
| :---------- | :---------------- | :---------------------------- |
| Scope       | Scope             | 授权范围                      |
| Cursor      | Cursor            | 游标分页定位符                |
| Idempotency | Idempotency       | 幂等性                        |
| RFC 5322    | RFC 5322          | 邮箱格式标准                  |
| E.164       | E.164             | 国际电话号码格式标准          |
| ISO 8601    | ISO 8601          | 时间表示标准                  |
| ISO 4217    | ISO 4217          | 货币代码标准                  |

### 10.4 参考文献

1. OpenAPI Initiative. (2021). _OpenAPI Specification 3.1.0_. https://spec.openapis.org/oas/v3.1.0
2. IETF. (2015). _RFC 7807: Problem Details for HTTP APIs_. https://datatracker.ietf.org/doc/html/rfc7807
3. IETF. (2021). _RFC 8941: Structured Field Values for HTTP_. https://datatracker.ietf.org/doc/html/rfc8941

---

## 📌 API 文档撰写 Checklist

- [ ] §0 文档导读：目的与适用范围 / 相关文档 / 变更记录
- [ ] §1 概述：基础 URL / 协议 / 版本 / 环境列表
- [ ] §2 认证授权：≥ 1 种认证方式 + Scope 模型 + 鉴权失败响应
- [ ] §3 通用约定：请求 / 响应信封 / 分页 / 命名 / HTTP 方法语义 / 幂等
- [ ] §4 端点列表：≥ 全部公开端点
- [ ] §5 端点详述：每个端点含路径参数 / 请求体 / 请求示例 / 成功响应 / 错误响应
- [ ] §6 数据模型：所有共享 Schema 含字段类型 / 必填 / 可空
- [ ] §7 错误码字典：通用 + 业务错误码，含 HTTP 状态码与 message
- [ ] §8 版本管理：兼容性承诺 / 废弃流程 / 变更分类表
- [ ] §9 安全限流：限流策略 / 配额 / 安全最佳实践
- [ ] §10 附录：SDK / Mock / 术语 / 参考文献
- [ ] 关联文档链接完整（TRD / 架构文档 / OpenAPI Spec）
- [ ] 所有示例可复制粘贴运行
