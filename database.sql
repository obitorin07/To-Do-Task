-- DROP DATABASE IF EXISTS TO_DO_TASK;
-- CREATE DATABASE IF NOT EXISTS to_do_task;

-- USE to_do_task;

-- -- dimension table
-- CREATE TABLE IF NOT EXISTS tasks (
--     task_id INT AUTO_INCREMENT PRIMARY KEY,
--     task_description VARCHAR(255) NOT NULL UNIQUE,
--     is_active BOOLEAN DEFAULT TRUE
-- );

-- --  task_logs table (fact table) without foreign key
-- CREATE TABLE IF NOT EXISTS task_logs (
--     log_id INT AUTO_INCREMENT PRIMARY KEY,
--     task_id INT,  -- No foreign key constraint
--     unique_task_number VARCHAR(50) UNIQUE,
--     week_number VARCHAR(50),
--     day_name VARCHAR(50),
--     task_date DATE,
--     task_time TIME,
--     is_completed BOOLEAN DEFAULT FALSE
-- );

-- --  some default tasks
-- INSERT IGNORE INTO tasks (task_description) VALUES 
-- ('Practice Data Analytics'),
-- ('Learn About Snowflake'),
-- ('Read Articles/Books'),
-- ('Practice Communication Skills');

USE TO_DO_TASK;
SELECT * FROM TASK_LOGS;
SELECT * FROM TASKS;
SELECT COUNT(*) AS TOTAL_RECORDS FROM TASK_LOGS;
SELECT * FROM TASK_LOGS WHERE TASK_DATE = (SELECT MAX(TASK_DATE) FROM TASK_LOGS);

-- DELETE FROM TASKS WHERE TASK_ID = 5;
-- TRUNCATE TASK_LOGS;
-- SELECT * FROM TASK_LOGS WHERE TASK_ID = 8;

with cte as(
	SELECT TASK_LOGS.* , TASKS.task_description FROM TASK_LOGS LEFT JOIN TASKS
	ON TASK_LOGS.TASK_ID = TASKS.TASK_ID)
SELECT 
	DAY_NAME AS DAY, 
	COUNT(*) AS TOTAL_TASKS_ASSIGNED, -- us din mene kitna task assign kiyata kudko :)
    SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) as No_of_Tasks_Complete
FROM CTE GROUP BY DAY_NAME  
