# [Product/System Name (English Name)] - Functional Requirements Document (FRD)

> **Document Status:** 🟡 Under Review / 🟢 Approved / 🔴 Rejected
>
> **Confidentiality Level:** Confidential / Internal / Public
>
> **Version:** vX.X
>
> **Date:** YYYY-MM-DD
>
> **Author:** [Name/Role]
>
> **Reviewer:** [Name/Role]
>
> **Audience:** [Role List]
>
> **Document Hierarchy:** MRD → PRD → **FRD** (this document)
>
> **Related MRD:** [MRD ID] · [MRD Version]
>
> **Related PRD:** [PRD ID] · [PRD Version]

---

## 0. Document Guide

### 0.1 Document Hierarchy

The FRD takes over from the PRD's product proposal and answers **"How is this feature implemented?"**, serving as the **single source of truth** for development, testing, and operations teams.

```mermaid
graph LR
    A[MRD / 'Market Opportunity & Users'] -->|Business Review Passed| B[PRD / 'Product Proposal & Interaction']
    B -->|Requirements Review Passed| C[FRD / 'Technical Implementation & Interfaces']
    C -->|Technical Review Passed| D[Development & Testing]
    D -->|Acceptance Passed| E[Gray Release]

    style C fill:#e3f2fd,stroke:#1565c0,stroke-width:4px
    style B fill:#fff3e0,stroke:#e65100
    style A fill:#f3e5f5,stroke:#7b1fa2
```

### 0.2 Related Documents

| Document Type | Filename              | Related Section   |
| ------------- | --------------------- | ----------------- |
| [Type]        | [Filename] [Line Range] | [Section Description] |

> **Reference Format Note**: Related documents use the `Filename Line Range` format (e.g., `【Template】Technical Requirements Document(TRD).md 3-17`). Line numbers may change as documents are updated; please refer to the actual content.

### 0.3 Change Log

| Version | Date       | Author  | Change Description                                            | Reviewer     |
| :------ | :--------- | :------ | :------------------------------------------------------------ | :----------- |
| v0.1    | YYYY-MM-DD | [Name]  | Initial draft completed                                       | [Architect]  |
| v0.2    | YYYY-MM-DD | [Name]  | Added exception flows and circuit breaker strategies          | [Architect]  |
| v1.0    | YYYY-MM-DD | [Name]  | Technical review passed, archived as baseline                 | [Tech Director] |
| v1.0.1  | 2026-06-09 | Xie Dong | Fixed xychart-beta diagram to table for Feishu compatibility  | —            |
| v1.0.2  | 2026-06-20 | Xie Dong | Updated middleware example RocketMQ→Pulsar (unified event bus spec) | —            |

---

## 1. Functional Overview

### 1.1 Function Definition

| Property       | Description                                                                                    |
| :------------- | :--------------------------------------------------------------------------------------------- |
| **Function Name** | [Module name, e.g., Smart Order Fulfillment Engine]                                           |
| **Function ID**   | FUNC-XXX                                                                                       |
| **Related PRD**   | [PRD ID-Section, e.g., PRD-2026-001 §3.2]                                                     |
| **Function Goal** | [One sentence: the core capability the system needs to implement, e.g., precise inventory deduction and order status consistency under high-concurrency scenarios] |
| **Business Value** | [Quantified value, e.g., support 100K TPS order placement during peak promotions, inventory oversell rate <<0.001%] |

### 1.2 Functional Landscape (Use Case)

```mermaid
graph LR
    subgraph External Participants
        U1[End User / C-side Consumer]
        U2[Merchant Operator / B-side Admin]
        U3[Internal System / ERP/WMS]
    end

    subgraph Function Boundary
        F1[Submit Order]
        F2[Query Order]
        F3[Cancel Order]
        F4[Modify Order Price]
        F5[Auto Warehouse Allocation]
    end

    subgraph External Dependencies
        D1[Payment Gateway]
        D2[Logistics Platform]
        D3[Message Push]
    end

    U1 --> F1
    U1 --> F2
    U1 --> F3
    U2 --> F4
    U3 --> F5
    F1 --> D1
    F5 --> D2
    F1 --> D3

    style F1 fill:#c8e6c9,stroke:#2e7d32
    style F3 fill:#ffcdd2,stroke:#c2185b
```

### 1.3 System Architecture

```mermaid
graph TB
    subgraph Access Layer
        A1[CDN/Static Resources]
        A2[API Gateway / Auth/Rate Limiting/Routing]
        A3[Load Balancing / SLB]
    end

    subgraph Service Layer
        B1[Order Service]
        B2[Inventory Service]
        B3[Pricing Service]
        B4[Promotion Service]
        B5[Fulfillment Service]
    end

    subgraph Middleware
        C1[(Redis / Distributed Lock/Cache)]
        C2[(Pulsar / Async Messaging)]
        C3[(ElasticJob / Scheduled Tasks)]
    end

    subgraph Data Layer
        D1[(PostgreSQL / Order DB - Sharded)]
        D2[(TiDB / Inventory Ledger)]
        D3[(OSS / Order Attachments)]
    end

    A2 --> A3
    A3 --> B1
    A3 --> B2
    A3 --> B3
    A3 --> B4
    B1 --> B2
    B1 --> B3
    B1 --> B4
    B1 --> C1
    B1 --> C2
    B2 --> C1
    B5 --> C2
    B5 --> C3
    B1 --> D1
    B2 --> D2
    B5 --> D3

    style B1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style C1 fill:#fff3e0,stroke:#e65100
    style D1 fill:#f3e5f5,stroke:#7b1fa2
```

---

## 2. Domain Model

### 2.1 Entity Relationship Diagram (ER)

```mermaid
erDiagram
    ORDER ||--o{ ORDER_ITEM : contains
    ORDER ||--|| PAYMENT : has
    ORDER ||--o{ ORDER_LOG : records
    ORDER_ITEM }o--|| SKU : references
    SKU ||--|| INVENTORY : tracks

    ORDER {
        string order_id PK "Order No. O2026xxxx"
        string user_id FK "User ID"
        int status "Status Enum"
        decimal total_amount "Order Total Amount"
        decimal pay_amount "Actual Payment Amount"
        datetime create_time "Creation Time"
        datetime expire_time "Expiration Time"
    }

    ORDER_ITEM {
        string item_id PK "Line ID"
        string order_id FK "Order No."
        string sku_id FK "SKU Code"
        int quantity "Quantity"
        decimal unit_price "Unit Price"
    }

    INVENTORY {
        string sku_id PK "SKU Code"
        int available_stock "Available Stock"
        int frozen_stock "Frozen Stock"
        int version "Optimistic Lock Version"
        datetime update_time "Update Time"
    }

    PAYMENT {
        string payment_id PK "Payment Transaction No."
        string order_id FK "Order No."
        int channel "Payment Channel"
        int status "Payment Status"
        decimal amount "Payment Amount"
    }
```

### 2.2 Domain Events

```mermaid
graph LR
    E1[OrderCreated] --> H1[Inventory Pre-occupy]
    E1 --> H2[Coupon Freeze]
    E1 --> H3[Message Notification]

    E2[OrderPaid] --> H4[Inventory Deduction]
    E2 --> H5[Generate Fulfillment Order]
    E2 --> H6[Points Issuance]

    E3[OrderCancelled] --> H7[Inventory Release]
    E3 --> H8[Coupon Return]
    E3 --> H9[Refund Initiation]

    style E1 fill:#e3f2fd,stroke:#1565c0
    style E2 fill:#c8e6c9,stroke:#2e7d32
    style E3 fill:#ffcdd2,stroke:#c2185b
```

---

## 3. Business Process

### 3.1 Core Flow (Happy Path)

```mermaid
flowchart TD
    Start([Start]) --> A[1. Receive Order Request]
    A --> B{2. Gateway Validation / Auth/Rate Limiting/Dedup}
    B -->|Failed| C[Return 401/429/403]
    B -->|Passed| D[3. Parameter Basic Validation]
    D -->|Failed| E[Return 400 Parameter Error]
    D -->|Passed| F[4. Distributed Lock / Prevent Concurrent Oversell]
    F -->|Lock Acquire Failed| G[Return 409 Operation Conflict]
    F -->|Lock Acquired| H[5. Inventory Validation]
    H -->|Insufficient Stock| I[Return 400 Insufficient Stock]
    H -->|Sufficient Stock| J[6. Price Calculation / Real-time Price & Promotions]
    J --> K[7. Create Order / Order Items & Payment Record]
    K --> L[8. Async Message / Inventory Pre-occupy/Notification]
    L --> M[9. Return Order Result]
    M --> End([End])

    C --> End
    E --> End
    G --> End
    I --> End

    style Start fill:#e1f5fe
    style End fill:#e1f5fe
    style M fill:#c8e6c9,stroke:#2e7d32,stroke-width:2px
    style C fill:#ffcdd2
    style E fill:#ffcdd2
    style G fill:#ffcdd2
    style I fill:#ffcdd2
```

### 3.2 Exception & Degradation Flows

```mermaid
flowchart TD
    A[Main Flow Exception] --> B{Exception Type}

    B -->|Downstream Timeout| C[Circuit Breaker Strategy]
    C --> C1[Pricing Service >500ms]
    C1 --> C2[Return Cached Price / Tolerance ±5%]
    C2 --> C3[Log & Alert / Manual Verification]

    B -->|Inventory Inconsistency| D[Reconciliation Compensation]
    D --> D1[Periodic Scan / Pre-occupied >15min unpaid]
    D1 --> D2[Auto Release Inventory]
    D2 --> D3[Coupon Return]

    B -->|Payment Callback Lost| E[Message Fallback]
    E --> E1[Polling Payment Status / Every 30s x 10 times]
    E1 -->|Still Failed| E2[Manual Ticket / CS Intervention]

    B -->|System Crash| F[Transaction Rollback]
    F --> F1[Order Creation Failed]
    F1 --> F2[Inventory Not Pre-occupied]
    F2 --> F3[Coupon Not Frozen]
    F3 --> F4[Idempotency Key Retained / Prevent Duplicate Submission]

    style C fill:#fff3e0,stroke:#e65100
    style D fill:#e3f2fd,stroke:#1565c0
    style E fill:#f3e5f5,stroke:#7b1fa2
```

### 3.3 Exception Scenario Matrix

| Error ID      | Scenario     | Trigger Condition             | System Behavior               | Error Code | User Prompt                    | Monitoring Alert |
| :------------ | :----------- | :---------------------------- | :---------------------------- | :--------: | :----------------------------- | :--------------: |
| TPL-ERR-001  | Missing Param | Required field empty          | Reject request, log           |   400001   | "Please complete required info" |        No        |
| TPL-ERR-002  | Duplicate Submit | Idempotency key already exists | Return previous result     |   200001   | "Operation successful"         |        No        |
| TPL-ERR-003  | Concurrent Conflict | Optimistic lock version mismatch | Prompt data has changed  |   409001   | "Data has been updated, please refresh and retry" | Yes |
| TPL-ERR-004  | Insufficient Stock | Available stock << purchase quantity | Reject order          |   400002   | "Insufficient stock, only X left" |      Yes       |
| TPL-ERR-005  | Dependency Timeout | Downstream service >500ms no response | Circuit break, return degraded data | 503001 | "Service busy, please try again later" | Yes |
| TPL-ERR-006  | Price Changed | Real-time price vs cached price diff >5% | Prompt price updated |   400003   | "Product price has been updated, please confirm" | No |

---

## 4. State Machine

### 4.1 Order State Transitions

```mermaid
stateDiagram-v2
    [*] --> CREATED: Submit Order
    CREATED --> PAID: Payment Success
    CREATED --> CANCELLED: User Cancel/Timeout Unpaid
    CREATED --> CLOSED: System Close Order (15min)

    PAID --> SHIPPED: Warehouse Ships
    PAID --> REFUNDING: User Requests Refund

    SHIPPED --> DELIVERED: Logistics Delivery Confirmed
    SHIPPED --> RETURNING: User Rejects Delivery

    DELIVERED --> COMPLETED: User Confirms Receipt (7d auto)
    DELIVERED --> REFUNDING: After-sales Request

    REFUNDING --> REFUNDED: Refund Completed
    REFUNDING --> REJECTED: Refund Rejected

    RETURNING --> RETURNED: Return to Warehouse
    CANCELLED --> [*]
    CLOSED --> [*]
    COMPLETED --> [*]
    REFUNDED --> [*]
    RETURNED --> [*]
    REJECTED --> COMPLETED

    note right of CREATED
        Timeout: 15 minutes
        Scheduled Task: ElasticJob scans every 1 minute
    end note

    note right of PAID
        Triggered after payment success:
        1. Official inventory deduction
        2. Generate fulfillment order
        3. Notify warehouse via message
    end note
```

### 4.2 State Transition Rules

| Current State | Target State | Trigger Event     | Pre-condition     | Post Action             | Permission |
| :------------ | :----------- | :---------------- | :---------------- | :---------------------- | :--------- |
| CREATED       | PAID         | Payment callback success | Amount match  | Deduct inventory, notify warehouse | System |
| CREATED       | CANCELLED    | User clicks cancel | Unpaid          | Release inventory, return coupon | Buyer |
| CREATED       | CLOSED       | Timeout close order | Created time >15min | Release inventory, return coupon | System |
| PAID          | SHIPPED      | Warehouse scan shipment | Inventory deducted | Update logistics tracking no. | Merchant |
| DELIVERED     | COMPLETED    | Auto confirm receipt | Delivery time >7d | Settle merchant, issue points | System |

---

## 5. Interface Definition

### 5.1 API Inventory

| API ID  | API Name     | Method | Path                              |     Caller      | Concurrency Target | Priority |
| :------ | :----------- | :----: | :-------------------------------- | :-------------: | :----------------- | :------: |
| API-001 | Create Order | POST   | `/api/v1/orders`                  | App/Web/Mini Program | 5000 TPS      |    P0    |
| API-002 | Query Order Detail | GET | `/api/v1/orders/{orderId}`     | App/Web/Mini Program | 10000 TPS     |    P0    |
| API-003 | Cancel Order | PUT    | `/api/v1/orders/{orderId}/cancel` |     App/Web     | 1000 TPS       |    P0    |
| API-004 | Order List   | GET    | `/api/v1/orders`                  |     App/Web     | 5000 TPS       |    P1    |
| API-005 | Payment Callback | POST | `/callback/payment`              |  Payment Gateway | 3000 TPS       |    P0    |

### 5.2 Detailed API: API-001 Create Order

#### 5.2.1 API Overview

| Item           | Description                                                              |
| :------------- | :----------------------------------------------------------------------- |
| **API Name**   | Create Order                                                             |
| **Request Path** | `POST /api/v1/orders`                                                  |
| **API Description** | User submits order; system validates inventory, price, and promotions, then creates order and returns the pending-payment order |
| **Idempotency** | Yes (ensured via `idempotency-key`)                                     |
| **Timeout**    | 3000ms                                                                   |
| **Degradation Strategy** | If pricing service times out, use cached price (tolerance ±5%)   |

#### 5.2.2 Request Headers

| Parameter         |  Type  | Required | Example                       | Description                                      |
| :---------------- | :----: | :------: | :---------------------------- | :----------------------------------------------- |
| Authorization     | string |   Yes    | `Bearer eyJhbG...`            | Access token                                     |
| X-Request-ID      | string |   Yes    | `req_20260525103000_abc123`   | Trace ID, globally unique                        |
| X-Idempotency-Key | string |   Yes    | `idem_user123_1625103000`     | Idempotency key; duplicate requests within 30 min return same result |
| Content-Type      | string |   Yes    | `application/json`            | Fixed value                                      |
| X-Client-Version  | string |   No     | `ios/3.2.1`                   | Client version, for compatibility handling        |

#### 5.2.3 Request Body

```json
{
  "skuList": [
    {
      "skuId": "SKU20260525001",
      "quantity": 2,
      "source": "cart"
    }
  ],
  "addressId": "ADDR123456",
  "couponId": "CPN789012",
  "remark": "Please ship as soon as possible, urgent",
  "source": "app_ios",
  "extInfo": {
    "deviceId": "device_abc123",
    "ip": "123.45.67.89"
  }
}
```

| Parameter   |  Type  | Required | Validation Rule                            | Description                          |
| :---------- | :----: | :------: | :----------------------------------------- | :----------------------------------- |
| skuList     | array  |   Yes    | Non-empty, length 1-50                     | Product list                         |
| └─ skuId    | string |   Yes    | Format: `SKU` + date + 3-digit sequence    | Product SKU                          |
| └─ quantity |  int   |   Yes    | 1~999                                      | Purchase quantity                    |
| └─ source   | string |   No     | Enum: `cart`/`direct`/`activity`           | Source: cart/direct purchase/activity |
| addressId   | string |   Yes    | Existing and valid address ID              | Shipping address                     |
| couponId    | string |   No     | Valid coupon ID                            | Coupon                               |
| remark      | string |   No     | Length ≤200, filter sensitive words        | Order remark                         |
| source      | string |   No     | Enum: `app_ios`/`app_android`/`web`/`mp`  | Client source                        |
| extInfo     | object |   No     | —                                          | Extended info, for risk control      |

#### 5.2.4 Response Body

**Success Response (200 OK):**

```json
{
  "code": 200,
  "message": "success",
  "traceId": "req_20260525103000_abc123",
  "data": {
    "orderId": "ORD202605250001",
    "status": "CREATED",
    "totalAmount": 299.0,
    "discountAmount": 30.0,
    "payAmount": 269.0,
    "itemCount": 2,
    "createTime": "2026-05-25T10:30:00+08:00",
    "expireTime": "2026-05-25T10:45:00+08:00",
    "paymentUrl": "https://pay.example.com/prepare?token=xxx"
  }
}
```

| Parameter      |  Type   | Description                                                                   |
| :------------- | :-----: | :---------------------------------------------------------------------------- |
| orderId        | string  | Unique order identifier, globally unique                                      |
| status         | string  | Order status: `CREATED`/`PAID`/`SHIPPED`/`DELIVERED`/`COMPLETED`/`CANCELLED` |
| totalAmount    | decimal | Order total amount (CNY)                                                      |
| discountAmount | decimal | Discount amount (CNY)                                                         |
| payAmount      | decimal | Actual payment amount (CNY)                                                   |
| itemCount      |   int   | Number of items                                                               |
| createTime     | string  | Creation time (ISO8601)                                                       |
| expireTime     | string  | Payment deadline (15 minutes)                                                 |
| paymentUrl     | string  | Payment redirect URL (only returned in CREATED status)                        |

**Error Response (400 Bad Request):**

```json
{
  "code": 400002,
  "message": "Insufficient stock",
  "traceId": "req_20260525103000_abc123",
  "data": {
    "skuId": "SKU20260525001",
    "availableStock": 1,
    "requestQuantity": 2
  }
}
```

#### 5.2.5 Error Code Reference

| Error Code | HTTP Status | Description        | Client Handling Suggestion                              |
| :--------: | :---------: | :----------------- | :------------------------------------------------------ |
|   400001   |     400     | Parameter validation failed | Check required fields and format                  |
|   400002   |     400     | Insufficient stock | Prompt insufficient stock, guide to reduce quantity or choose other products |
|   400003   |     400     | Coupon unavailable | Prompt coupon expired/not applicable/already used  |
|   400004   |     400     | Invalid shipping address | Guide user to re-select address                  |
|   401001   |     401     | Login session expired | Redirect to login page                            |
|   429001   |     429     | Too many requests | Show countdown, limit submission frequency              |
|   409001   |     409     | Concurrent operation conflict | Prompt "Data has been updated, please refresh and retry" |
|   500001   |     500     | Internal server error | Show friendly error page, report logs              |
|   503001   |     503     | Downstream service busy | Prompt "Service busy, please try again later", suggest retry after 3 seconds |

---

## 6. Data Flow & Interaction Sequence

### 6.1 Core Order Placement Sequence

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant C as Client
    participant GW as API Gateway / Auth/Rate Limiting/Dedup
    participant OS as Order Service
    participant IS as Inventory Service
    participant PS as Pricing Service
    participant CS as Promotion Service
    participant DB as Order DB / PostgreSQL
    participant RC as Cache / Redis
    participant MQ as Message Queue / Pulsar

    U->>C: Submit Order
    C->>GW: POST /api/v1/orders with Token and Idempotency-Key
    GW->>GW: JWT verification and rate limiting check

    alt Rate Limiting Triggered
        GW-->>C: 429 Too Many Requests
        C-->>U: Prompt operation too frequent
    else Passed
        GW->>OS: Forward Request

        OS->>OS: Parameter basic validation

        OS->>RC: SET order_lock:{userId} NX EX 10
        alt Lock Acquire Failed
            RC-->>OS: Already exists
            OS-->>GW: 409 Operation Conflict
            GW-->>C: Return conflict prompt
        else Lock Acquired
            OS->>IS: Validate and pre-occupy inventory
            IS->>RC: DECR available_stock / INCR frozen_stock
            IS->>IS: Write inventory ledger
            IS-->>OS: Pre-occupy success

            OS->>PS: Get real-time price
            alt Pricing Service Timeout >500ms
                OS->>RC: Read cached price
                OS->>OS: Mark price for verification
            else Normal Response
                PS-->>OS: Return real-time price
            end

            opt Using Coupon
                OS->>CS: Validate and freeze coupon
                CS-->>OS: Freeze success
            end

            OS->>DB: Begin Transaction
            OS->>DB: INSERT Order Master Table
            OS->>DB: INSERT Order Items Table
            OS->>DB: INSERT Payment Record
            DB-->>OS: Return Order ID

            OS->>MQ: Send OrderCreated Event
            Note over MQ: Async: notify warehouse / send SMS/push / update analytics

            OS->>RC: DEL order_lock:{userId}
            OS-->>GW: Return Order Details
            GW-->>C: 200 OK with Order Data
            C-->>U: Display Pending-Payment Order
        end
    end
```

### 6.2 Payment Callback Sequence

```mermaid
sequenceDiagram
    autonumber
    participant PG as Payment Gateway
    participant GW as API Gateway
    participant OS as Order Service
    participant DB as Order DB
    participant MQ as Message Queue
    participant FS as Fulfillment Service
    participant WH as Warehouse System

    PG->>GW: POST /callback/payment / Payment Result Notification
    GW->>GW: Signature verification and anti-replay

    GW->>OS: Forward Callback
    OS->>DB: Query Order Status
    alt Order Already Paid/Cancelled
        OS-->>GW: Return 200 (idempotent)
    else Order Pending Payment
        OS->>DB: Begin Transaction
        OS->>DB: UPDATE Order Status to PAID
        OS->>DB: UPDATE Payment Record Status to SUCCESS
        OS->>DB: COMMIT

        OS->>MQ: Send OrderPaid Event

        MQ->>FS: Consume Event
        FS->>WH: Create Fulfillment Order
        FS->>MQ: Send FulfillmentCreated

        OS-->>GW: Return 200 Success
    end
    GW-->>PG: 200 Success (callback caller requires 200 response)
```

---

## 7. Non-Functional Requirements (NFR / SLA)

### 7.1 Performance Metrics

> **Note**: xychart-beta is an incompatible Mermaid type for Feishu; replaced with table description (template sample data).

**API Performance Targets (P99 Response Time ms)**

| API         | P99 Response Time (ms) |
| :---------- | :---------------------: |
| API-001 Create |          300           |
| API-002 Query  |          100           |
| API-003 Cancel |          200           |
| API-004 List   |          150           |

| Metric Item              | Target Value | Measurement Method        | Owner  |
| :----------------------- | :----------- | :------------------------ | :----- |
| Core API P99 Latency     | ≤ 300ms      | APM Monitoring (SkyWalking) | Backend |
| Query API P99 Latency    | ≤ 100ms      | APM Monitoring            | Backend |
| Concurrency Capacity     | ≥ 5000 TPS   | Full-chain Load Testing   | Architecture |
| Database QPS             | ≥ 10000      | Slow Query Monitoring     | DBA    |
| Cache Hit Rate           | ≥ 95%        | Redis Monitoring          | Backend |

### 7.2 Availability & Reliability

| Metric Item       | Target Value                | Implementation Method                    |
| :---------------- | :-------------------------- | :---------------------------------------- |
| System Availability | ≥ 99.95%                   | Multi-active deployment + automatic failover |
| Data Consistency  | Strong consistency (order/inventory/payment) | Distributed transactions (Seata AT mode) |
| Data Persistence  | RPO=0, RTO<<30s            | Master-slave sync + automatic switchover  |
| Degradation Capability | Critical path degradable | Circuit breaker (Sentinel) + fallback cache |

### 7.3 Security & Compliance

| Item             | Requirement                              | Verification Method    |
| :--------------- | :--------------------------------------- | :--------------------- |
| Transport Encryption | TLS 1.3                              | SSL Labs scan          |
| Sensitive Data   | Phone/ID AES-256 encrypted storage       | Security audit         |
| Anti-Replay Attack | Timestamp + nonce + signature, 5 min validity | Penetration testing |
| Access Control   | RBAC + data permission isolation          | Automated permission scan |
| Audit Log        | All financial operations logged, retained 180 days | Log audit   |

---

## 8. Acceptance Criteria

### 8.1 Functional Acceptance (Given-When-Then)

| AC-ID  | Acceptance Criteria (Gherkin Format)                                                                                                                                    |   Test Type    | Pass Criteria |
| :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------: | :-----------: |
| AC-001 | **Given** user is logged in and cart has 2 items<br>**When** user submits order with valid address<br>**Then** system creates order with status CREATED<br>**And** returns payment link valid within 15 minutes |  Integration Test | 100% Pass |
| AC-002 | **Given** product stock is only 1<br>**When** user attempts to purchase 2<br>**Then** system rejects order<br>**And** returns error code 400002<br>**And** inventory not pre-occupied |  Exception Test | 100% Pass |
| AC-003 | **Given** user has submitted order but not paid<br>**When** 15 minutes later the system close-order task executes<br>**Then** order status becomes CLOSED<br>**And** inventory auto-released<br>**And** coupon auto-returned | Scheduled Task Test | 100% Pass |
| AC-004 | **Given** 1000 concurrent users purchasing the same SKU simultaneously<br>**When** stock is 500<br>**Then** successful order count = 500<br>**And** no overselling<br>**And** no duplicate charges |  Concurrency Test | 100% Pass |
| AC-005 | **Given** pricing service response >500ms<br>**When** user submits order<br>**Then** system uses cached price<br>**And** order created successfully<br>**And** price difference alert triggered |  Degradation Test | 100% Pass |

### 8.2 Performance Acceptance

| Test ID  | Scenario                   | Target                               | Test Tool          |
| :------- | :------------------------- | :----------------------------------- | :----------------- |
| Load-001 | Create Order API           | 5000 TPS, P99<<300ms, error rate<<0.1% | JMeter/Gatling |
| Load-002 | Mixed Scenario (Query/Create/Cancel) | 10000 TPS, system load<<70%   | Full-chain Load Testing Platform |
| Load-003 | Database Capacity          | Single table 100M rows, query P99<<100ms | Capacity Test |

---

## 9. Release & Gray Release Plan

### 9.1 Gray Release Strategy

```mermaid
graph LR
    A[Internal Test / 1% employees & seed users] --> B[Whitelist / 10% invited merchants]
    B --> C[Regional Gray / 30% South China users]
    C --> D[Full Release / 100% users]
    D --> E[Monitor & Observe / 72 hours]

    A -->|Observe 3 days / No P0 Bug| B
    B -->|Observe 5 days / Core metrics normal| C
    C -->|Observe 7 days / No abnormal alerts| D

    style A fill:#fff3e0,stroke:#e65100
    style D fill:#c8e6c9,stroke:#2e7d32,stroke-width:3px
```

### 9.2 Release Checklist

| Stage     | Check Item                         | Owner     | Status |
| :-------- | :--------------------------------- | :-------- | :----: |
| Pre-release | Code Review passed (≥2 people)   | Tech Lead |  ⬜   |
| Pre-release | Unit test coverage ≥80%          | Dev       |  ⬜   |
| Pre-release | Interface contract test passed    | QA        |  ⬜   |
| Pre-release | DB migration script review passed | DBA       |  ⬜   |
| Pre-release | Monitoring dashboard/alert rules configured | SRE |  ⬜   |
| During Release | Blue-green deployment, traffic switch 10%→50%→100% | SRE | ⬜ |
| Post-release | Core API P99 latency monitoring  | SRE       |  ⬜   |
| Post-release | Error rate <<0.1% sustained 30 min | SRE     |  ⬜   |
| Post-release | Business metrics (order success rate) no decline | Product | ⬜ |

### 9.3 Rollback Strategy

| Trigger Condition        | Rollback Action                           | Rollback Time Target | Owner |
| :----------------------- | :---------------------------------------- | :------------------- | :---- |
| P0 Bug affecting >1% users | Immediately switch traffic to old version | ≤ 5 minutes          | SRE   |
| Performance degradation >50% | Degrade non-critical paths, preserve core ordering | ≤ 3 minutes | SRE |
| Database anomaly          | Pause writes, switch to read-only mode, manual intervention | ≤ 10 minutes | DBA |

---

## 10. Appendix

- **Appendix A:** Database migration scripts (DDL/DML)
- **Appendix B:** Interface contract test case set
- **Appendix C:** Load test report template and historical baselines
- **Appendix D:** Third-party service integration docs (Payment/Logistics/SMS)
- **Appendix E:** Glossary and data dictionary

> **FRD Writing Principles (Industry Standard):**
>
> 1. **Testability**: Every functional point must correspond to at least one AC (acceptance criterion).
> 2. **Observability**: Every API must define traceId, error code, and monitoring instrumentation.
> 3. **Rollback-ability**: Every change must consider rollback plans; data changes must be compatible with previous versions.
> 4. **Defensiveness**: Every external dependency must have timeout, circuit breaker, and degradation strategies.
> 5. **Consistency**: State machines must cover the full lifecycle; "hover states" are prohibited.
