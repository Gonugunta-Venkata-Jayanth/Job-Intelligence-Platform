# 📌 Database Schema – Job Intelligence Platform

The Job Intelligence Platform uses a **relational schema** optimized for analytics and fast querying by skills, salary, companies, and job titles.

---

## 🗄 Entity–Relationship Diagram (ERD)
```
companies (1) ────── () jobs ────── () job_skills ────── (1) skills

└──────── (1) locations
```

---

## 🔹 Tables & Fields

### **1. companies**
| Column        | Type | Description |
|--------------|------|-------------|
| id (PK)      | int  | Unique company ID |
| name         | text | Company name |

---

### **2. locations**
| Column         | Type | Description |
|---------------|------|-------------|
| id (PK)       | int  | Location ID |
| city          | text | City |
| state         | text | State |
| country       | text | Country |

---

### **3. jobs**
| Column             | Type | Description |
|-------------------|------|-------------|
| id (PK)           | int  | Job ID |
| title             | text | Job title |
| description       | text | Full job description |
| url               | text | Source link |
| salary_min        | int  | Actual min salary (if provided) |
| salary_max        | int  | Actual max salary (if provided) |
| salary_pred_min   | int  | Predicted min salary |
| salary_pred_max   | int  | Predicted max salary |
| date_posted       | date | Posting date |
| company_id (FK)   | int  | Reference to companies table |
| location_id (FK)  | int  | Reference to locations table |

---

### **4. skills**
| Column      | Type | Description |
|------------|------|-------------|
| id (PK)    | int  | Skill ID |
| skill_name | text | Normalized skill name |

---

### **5. job_skills**
| Column        | Type | Description |
|--------------|------|-------------|
| id (PK)      | int  | Job–skill mapping ID |
| job_id (FK)  | int  | Reference to jobs table |
| skill_id (FK)| int  | Reference to skills table |

---

## 🔥 Design Rationale

| Requirement | Design Decision |
|------------|------------------|
| Fast skill-based filtering | Dedicated many-to-many skills mapping |
| Efficient analytics | Normalized design prevents duplication |
| Scalability | De-duplicates companies & locations |
| AI salary prediction | Stored alongside actual values |

---

## ⏳ Next Enhancements

| Suggestion | Benefit |
|------------|---------|
| Add job type (remote/onsite/hybrid) | Better filtering |
| Add experience level | Targeted insights |
| Introduce indexes on `skills` and `company_id` | Faster querying |

---

