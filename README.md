![alt text](<Entire flow.png>)
# System Flow (Auth Service + Core Service)

This project follows a microservices architecture with two main services:

- **Auth Service** → Handles authentication (who you are)
- **Core Service** → Handles data (what you own)
- **JWT Token** → Connects both services

---

## Overall Flow

Client (Frontend)
        ↓
Login / Register (Auth Service)
        ↓
JWT Tokens Generated (Access + Refresh)
        ↓
Client stores tokens
        ↓
Client sends request with Access Token
        ↓
Core Service verifies token
        ↓
Core Service processes request
        ↓
Response sent back to client

---

## Auth Service Flow

### 1. User Registration
- User sends email, name, password
- Password is **hashed with salt (SHA-256)**
- Data stored securely in database
- Password is never returned

### 2. User Login
- User provides email and password
- Password is verified
- Two tokens are generated:
  - **Access Token** (valid for 30 minutes)
  - **Refresh Token** (valid for 7 days)

### 3. Token Usage
- Access token is used for API calls
- Each request is verified:
  - Token signature checked
  - Expiry checked
  - User status checked

### 4. Token Refresh
- If access token expires:
  - Client sends refresh token
  - New tokens are generated

### 5. Authorization (Permissions)
- Users get permissions using:
  - **Roles** (admin, manager, user)
  - **Types** (organization, team)
  - **Assignments** (link user + role + resource)

### 6. Soft Delete
- Data is not permanently deleted
- `deleted_at` timestamp is set
- Only active records (`deleted_at = 0`) are used

---

## Core Service Flow

### 1. Authentication
- Every request must include JWT token
- Token is decoded to get `user_id`

### 2. Organization Management
- Create organization
- Check for duplicates
- Store basic details

### 3. Team Management
- Teams belong to organizations
- Organization must exist
- Team count is automatically updated

### 4. Member Management
- Members are linked using:
  - `team_id`
  - `auth_user_id` (from Auth Service)
- No user data is stored here (only ID)

### 5. Data Handling
- Uses separate database
- Only manages:
  - Organizations
  - Teams
  - Members

### 6. Soft Delete
- Same as Auth Service
- Records are hidden, not removed

---

##  How Auth and Core Services Connect

Auth Service          Core Service
     │                     │
     │   JWT Token          │
     └─────────────────────┘
        Shared Secret Key

- Auth Service generates JWT token
- Core Service verifies token using same secret key
- `user_id` from token is used to link data

---

##  Key Concepts

### Users
- People who register in the system

### Roles
- Define permissions (admin, manager, user)

### Types
- Define level (organization or team)

### Assignments
- Connect:
  - User + Role + Type + Resource

---



##  Request Flow (Detailed)

Client Request
    ↓
CORS Middleware
    ↓
Logging Middleware
    ↓
Router (API endpoint)
    ↓
Token Verification
    ↓
Service Layer (Business Logic)
    ↓
Database Query
    ↓
Response वापस Client

---

##  Security Highlights

- Passwords are hashed with salt
- JWT tokens are verified on every request
- Access tokens expire quickly
- Refresh tokens provide new access
- Sensitive data is never exposed

---

##  Architecture Summary

- Microservices-based design
- Two independent databases
- Stateless authentication using JWT
- Scalable and secure system