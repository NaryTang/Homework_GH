CREATE DATABASE Housing_db;

USE Housing_db;

SELECT * FROM census_data;

CREATE TABLE annual_data
SELECT c.Year, c.Total_Households, c.Single_Male_Households, c.Single_Female_Households, s.Total_Student_Loans_Billions
FROM census_data AS c 
JOIN student_loan_data AS s
USING (Year)
GROUP BY Year;

SELECT * FROM annual_data;

