CREATE TABLE companies (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, website VARCHAR(255), created_at TIMESTAMP DEFAULT NOW());
CREATE TABLE locations (id SERIAL PRIMARY KEY, city VARCHAR(100), state VARCHAR(100), country VARCHAR(100), raw_location TEXT);
CREATE TABLE jobs (id SERIAL PRIMARY KEY, external_id VARCHAR(255),source VARCHAR(100),title VARCHAR(255) NOT NULL,company_id INT REFERENCES companies(id), location_id INT REFERENCES locations(id), posted_date DATE, scraped_at TIMESTAMP DEFAULT NOW(), url TEXT, description TEXT, min_salary NUMERIC, max_salary NUMERIC, currency VARCHAR(10), salary_pred_min NUMERIC, salary_pred_max NUMERIC);
CREATE TABLE skills (id SERIAL PRIMARY KEY, name VARCHAR(100) UNIQUE);

CREATE TABLE job_skills (job_id INT REFERENCES jobs(id) ON DELETE CASCADE, skill_id INT REFERENCES skills(id) ON DELETE CASCADE, source VARCHAR(50),PRIMARY KEY (job_id, skill_id));