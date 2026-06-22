#sql
USE retail_db;

CREATE VIEW user_cohort AS
SELECT 
    CustomerID,
    DATE_FORMAT(InvoiceDate, '%Y-%m') AS InvoiceMonth,
    DATE_FORMAT(
        MIN(InvoiceDate) OVER (PARTITION BY CustomerID), 
        '%Y-%m'
    ) AS CohortMonth,
    PERIOD_DIFF(  #`PERIOD_DIFF` 是 MySQL 计算两个年月之间相差月数的函数，结果就是用户距离首次购买过了几个月。
        DATE_FORMAT(InvoiceDate, '%Y%m'),
        DATE_FORMAT(MIN(InvoiceDate) OVER (PARTITION BY CustomerID), '%Y%m')
    ) AS MonthIndex
FROM orders;