-- financeapp.customer definition

CREATE TABLE `customer` (
  `CustomerID` int NOT NULL,
  `FirstName` varchar(45) DEFAULT NULL,
  `LastName` varchar(45) DEFAULT NULL,
  `Address` varchar(200) DEFAULT NULL,
  `EmailID` varchar(100) DEFAULT NULL,
  `Mobile` bigint DEFAULT NULL,
  `DateOfBirth` date DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE KEY `CustomerID_UNIQUE` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- financeapp.financedata definition

CREATE TABLE `financedata` (
  `CustomerID` int DEFAULT NULL,
  `AccEntryDate` date DEFAULT NULL,
  `AccEntryItemDesc` varchar(100) DEFAULT NULL,
  `Amount` decimal(12,2) DEFAULT NULL,
  `AccEntryType` varchar(100) DEFAULT NULL,
  `AccEntrySubType` varchar(100) DEFAULT NULL,
  KEY `financedata_FK` (`CustomerID`),
  CONSTRAINT `financedata_FK` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;