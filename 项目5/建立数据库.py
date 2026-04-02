#sql
CREATE DATABASE IF NOT EXISTS retail_db DEFAULT CHARSET utf8mb4;
USE retail_db;

CREATE TABLE orders (
    InvoiceNo VARCHAR(20),
    StockCode VARCHAR(20),
    Description VARCHAR(200),
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DECIMAL(10,2),
    CustomerID INT,
    Country VARCHAR(50)
);
