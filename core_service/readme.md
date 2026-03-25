# 🏢 Core Service

##  Purpose
Core Service is responsible for **business data management**.

It answers:
 What do you own?  
 What organizations and teams exist?

---

##  Responsibilities

- Organization Management
- Team Management
- Member Management
- Data relationships

---

##  Flow

### 1. Authentication
Client sends request with JWT token  
↓  
Token is decoded  
↓  
Extract user_id  
↓  
Request allowed

---

### 2. Create Organization
Client → sends name, description  
↓  
Check duplicate  
↓  
Create organization  
↓  
Set:
- teams_count = 0
- members_count = 0  
↓  
Save to database

---

### 3. Create Team
Client → sends team data  
↓  
Check organization exists  
↓  
Check duplicate team  
↓  
Create team  
↓  
Update organization team count  
↓  
Save

---

### 4. Add Member
Client → sends auth_user_id  
↓  
Check team exists  
↓  
Check member not already added  
↓  
Create member record  
↓  
Save

---

### 5. List Data
Client → requests teams or organizations  
↓  
Fetch from database  
↓  
Return list with count

---

### 6. Soft Delete

- Records are not removed  
- `deleted_at` timestamp updated  
- Hidden from future queries  

---

##  Connection with Auth Service

- Core Service does NOT store user data
- It only stores:
  - `auth_user_id`

Flow:
Auth Service → generates JWT  
↓  
Client sends token  
↓  
Core Service decodes token  
↓  
Gets user_id  

---

##  Key Concepts

### Organization
- Top-level entity

### Team
- Belongs to organization

### Member
- Links user to team

---

##  Database

Tables:
- organizations
- teams
- members

---

##  Security

- JWT required for every request
- Token verified using shared secret
- No sensitive user data stored

---

##  Summary

- Handles business data
- Uses user_id from Auth Service
- Fully separated from authentication