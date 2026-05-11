# Software Re-Engineering Project: Traccar & HealthBridge Hospital

This repository contains the complete execution of a software re-engineering project, divided into Code Analysis (Traccar) and Database Re-engineering (HealthBridge Hospital).

## 📂 Project Structure

- **`/Traccar`**: Open-source Java project used for Static and Dynamic analysis.
- **`/Database`**: Database re-engineering artifacts, including Prisma schema and ETL scripts.
  - `migration_etl.py`: Python script for migrating legacy CSV data to the refactored schema.
  - `schema.prisma`: The refactored relational database model.
  - `legacy_appointments.csv`: Sample legacy data used for migration testing.

## 🛠️ Setup and Execution

### 1. Static Code Analysis (SonarQube)
To reproduce the static analysis:
1. Ensure Docker is running.
2. Start SonarQube: `docker run -d --name sonarqube -p 9000:9000 sonarqube:latest`
3. Navigate to the `/Traccar` directory.
4. Run the scanner: `sonar-scanner`
5. View results at `http://localhost:9000`

### 2. Database Re-engineering (Prisma)
To set up the refactored hospital database:
1. Navigate to the `/Database` directory.
2. Install dependencies: `npm install`
3. Push the schema to your local MySQL instance: `npx prisma db push`

### 3. Data Migration (ETL Pipeline)
To migrate legacy data:
1. Ensure your MySQL database is running and `hospital_db` is created.
2. Update the credentials in `Database/migration_etl.py` (lines 73-78).
3. Run the migration script: `python Database/migration_etl.py`

## 📊 Analysis Highlights
- **Part B (Code Smells):** Identified Bloaters (Long Method), OO Abusers (Switch Statements), and Couplers (Message Chains) in the Traccar project.
- **Part C (Metrics):** Calculated Instability (I) for core classes and prioritized Technical Debt remediation.
- **Part D (Dynamic Analysis):** Performed execution tracing on `Checksum.luhn()` and generated Control Flow Graphs (CFG).
- **Part E & F (Database):** Normalized the legacy hospital schema to 3NF and implemented structural refactoring scripts.

---
**Course:** Software Re-Engineering (SRE)  
**Project Objective:** Complete Re-Engineering Lifecycle
