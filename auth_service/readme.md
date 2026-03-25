# 🔐 Auth Service

##  Purpose
Auth Service is responsible for **authentication and authorization**.

It answers:
 Who are you?  
 Are you allowed to access the system?

---

##  Responsibilities

- User Registration
- User Login
- Password Security (Hashing + Salt)
- JWT Token Generation
- Token Verification
- Role-Based Access Control (RBAC)

---

##  Flow

### 1. User Registration
Client → sends email, name, password  
↓  
Validate input  
↓  
Generate salt  
↓  
Hash password (SHA-256)  
↓  
Store user in database  
↓  
Return user (without password)

---

### 2. User Login
Client → sends email + password  
↓  
Find user in database  
↓  
Verify password  
↓  
Generate:
- Access Token (30 mins)
- Refresh Token (7 days)  
↓  
Return tokens

---

### 3. Token Usage
Client → sends request with:
Authorization: Bearer <access_token>  
↓  
Token is verified:
- Signature checked  
- Expiry checked  
- User existence checked  
↓  
Request allowed

---

### 4. Token Refresh
Access token expired  
↓  
Client sends refresh token  
↓  
Verify refresh token  
↓  
Generate new tokens  
↓  
Return new tokens

---

### 5. Authorization (RBAC)

Permissions are managed using:

- **Users** → people in system  
- **Roles** → admin, manager, user  
- **Types** → organization, team  
- **Assignments** → link user + role + resource  

Example:
- John → admin → organization  
- John → manager → team  

---

### 6. Soft Delete

- Records are NOT deleted permanently  
- `deleted_at` is updated  
- Queries use:
  WHERE deleted_at = 0  

---

##  Key Concepts

### Users
- Registered accounts
- Have email, name, password

### Roles
- Define permissions
- admin / manager / user

### Types
- Define level:
  - organization
  - team

### Assignments
- Connect user + role + resource

---

##  Security

- Passwords are hashed (SHA-256 + salt)
- Password never returned in response
- JWT tokens used for authentication
- Tokens verified on every request

---

##  Database

Tables:
- users
- roles
- types
- assignments

---

##  Summary

- Handles identity and access
- Generates JWT tokens
- Ensures secure authentication