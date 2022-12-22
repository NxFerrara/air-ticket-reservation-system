-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 22, 2022 at 06:52 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `air_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `AirlineName` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`AirlineName`) VALUES
('United');

-- --------------------------------------------------------

--
-- Table structure for table `airlinestaff`
--

CREATE TABLE `airlinestaff` (
  `Username` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) NOT NULL,
  `DateofBirth` date NOT NULL,
  `AirlineName` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airlinestaff`
--

INSERT INTO `airlinestaff` (`Username`, `Password`, `FirstName`, `LastName`, `DateofBirth`, `AirlineName`) VALUES
('admin', 'e2fc714c4727ee9395f324cd2e7f331f', 'Roe', 'Jones', '1978-05-25', 'United'),
('jd123', '81dc9bdb52d04dc20036dbd8313ed055', 'Joe', 'Dan', '2022-11-16', 'United');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `IDNumber` int(11) NOT NULL,
  `NumberofSeats` int(11) NOT NULL,
  `ManufacturingCompany` varchar(50) NOT NULL,
  `Age` int(11) NOT NULL,
  `AirlineName` varchar(50) NOT NULL,
  `NumberofEconomyClassSeats` int(11) NOT NULL,
  `NumberofBusinessClassSeats` int(11) NOT NULL,
  `NumberofFirstClassSeats` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`IDNumber`, `NumberofSeats`, `ManufacturingCompany`, `Age`, `AirlineName`, `NumberofEconomyClassSeats`, `NumberofBusinessClassSeats`, `NumberofFirstClassSeats`) VALUES
(1, 4, 'Boeing', 10, 'United', 2, 1, 1),
(2, 4, 'Airbus', 12, 'United', 2, 1, 1),
(3, 50, 'Boeing', 8, 'United', 30, 15, 5),
(5, 4, 'Boeing', 5, 'United', 2, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `AirportName` varchar(50) NOT NULL,
  `City` varchar(50) NOT NULL,
  `Country` varchar(50) NOT NULL,
  `AirportType` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`AirportName`, `City`, `Country`, `AirportType`) VALUES
('BEI', 'Beijing', 'China', 'Both'),
('BOS', 'Boston', 'USA', 'Both'),
('HKA', 'Hong Kong', 'China', 'Both'),
('JFK', 'NYC', 'USA', 'Both'),
('LAX', 'Los Angeles', 'USA', 'Both'),
('ORD', 'Orlando', 'USA', 'Both'),
('PVG', 'Shanghai', 'China', 'Both'),
('SFO', 'San Francisco', 'USA', 'Both'),
('SHEN', 'Shenzhen', 'China', 'Both');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `Name` varchar(50) NOT NULL,
  `EmailAddress` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `BuildingNumber` int(11) NOT NULL,
  `Street` varchar(50) NOT NULL,
  `City` varchar(50) NOT NULL,
  `State` varchar(50) NOT NULL,
  `PhoneNumber` varchar(50) NOT NULL,
  `PassportNumber` int(11) NOT NULL,
  `PassportExpiration` date NOT NULL,
  `PassportCountry` varchar(50) NOT NULL,
  `DateofBirth` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`Name`, `EmailAddress`, `Password`, `BuildingNumber`, `Street`, `City`, `State`, `PhoneNumber`, `PassportNumber`, `PassportExpiration`, `PassportCountry`, `DateofBirth`) VALUES
('Test Customer 1', 'testcustomer@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 1555, 'Jay St', 'Brooklyn', 'New York', '123-4321-4321', 54321, '2025-12-24', 'USA', '1999-12-19'),
('User 1', 'user1@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 5405, 'Jay Street', 'Brooklyn', 'New York', '123-4322-4322', 54322, '2025-12-25', 'USA', '1999-11-19'),
('User 2', 'user2@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 1702, 'Jay Street', 'Brooklyn', 'New York', '123-4323-4323', 54323, '2025-10-24', 'USA', '1999-09-19'),
('User 3', 'user3@nyu.edu', '81dc9bdb52d04dc20036dbd8313ed055', 1890, 'Jay Street', 'Brooklyn', 'New York', '123-4324-4324', 54324, '2025-09-24', 'USA', '1999-09-19');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `FlightNumber` varchar(50) NOT NULL,
  `DepartureDateandTime` datetime NOT NULL,
  `ArrivalDateandTime` datetime NOT NULL,
  `BasePrice` float NOT NULL,
  `Status` varchar(50) NOT NULL,
  `DepartureAirportName` varchar(50) NOT NULL,
  `ArrivalAirportName` varchar(50) NOT NULL,
  `IDNumber` int(11) NOT NULL,
  `AirlineName` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`FlightNumber`, `DepartureDateandTime`, `ArrivalDateandTime`, `BasePrice`, `Status`, `DepartureAirportName`, `ArrivalAirportName`, `IDNumber`, `AirlineName`) VALUES
('102', '2022-09-12 13:25:25', '2022-09-12 16:50:25', 300, 'on-time', 'SFO', 'LAX', 3, 'United'),
('104', '2022-10-04 13:25:25', '2022-10-04 16:50:25', 300, 'on-time', 'PVG', 'BEI', 3, 'United'),
('106', '2022-08-04 13:25:25', '2022-08-04 16:50:25', 350, 'delayed', 'SFO', 'LAX', 3, 'United'),
('134', '2022-07-12 13:25:25', '2022-07-12 16:50:25', 300, 'delayed', 'JFK', 'BOS', 3, 'United'),
('206', '2023-02-04 13:25:25', '2023-02-04 16:50:25', 400, 'on-time', 'SFO', 'LAX', 2, 'United'),
('207', '2023-03-04 13:25:25', '2023-03-04 16:50:25', 300, 'on-time', 'LAX', 'SFO', 2, 'United'),
('296', '2022-12-30 13:25:25', '2022-12-30 16:50:25', 3000, 'Delayed', 'PVG', 'SFO', 1, 'United'),
('532', '2022-12-18 10:30:55', '2022-12-18 14:30:55', 700, 'On-time', 'SFO', 'ORD', 5, 'United'),
('715', '2022-09-28 10:25:25', '2022-09-28 13:50:25', 500, 'delayed', 'PVG', 'BEI', 1, 'United'),
('839', '2021-12-26 13:25:25', '2021-12-26 16:50:25', 300, 'on-time', 'SHEN', 'BEI', 3, 'United');

-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

CREATE TABLE `purchase` (
  `TicketIDNumber` int(11) NOT NULL,
  `EmailAddress` varchar(50) NOT NULL,
  `PurchaseDateandTime` datetime NOT NULL,
  `CardNumber` varchar(50) NOT NULL,
  `CardType` varchar(50) NOT NULL,
  `NameonCard` varchar(50) NOT NULL,
  `ExpirationDate` date NOT NULL,
  `sold_price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`TicketIDNumber`, `EmailAddress`, `PurchaseDateandTime`, `CardNumber`, `CardType`, `NameonCard`, `ExpirationDate`, `sold_price`) VALUES
(1, 'testcustomer@nyu.edu', '2022-08-04 11:55:55', '1111-2222-3333-4444', 'Credit', 'Test Customer 1', '2023-03-01', 300),
(2, 'user1@nyu.edu', '2022-08-03 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 1', '2023-03-01', 300),
(3, 'user2@nyu.edu', '2022-09-04 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 2', '2023-03-01', 300),
(4, 'user1@nyu.edu', '2022-08-21 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 1', '2023-03-01', 300),
(5, 'testcustomer@nyu.edu', '2022-09-28 11:55:55', '1111-2222-3333-4444', 'Credit', 'Test Customer 1', '2023-03-01', 300),
(6, 'testcustomer@nyu.edu', '2022-08-02 11:55:55', '1111-2222-3333-4444', 'Credit', 'Test Customer 1', '2023-03-01', 350),
(7, 'user3@nyu.edu', '2022-07-03 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 3', '2023-03-01', 300),
(8, 'user3@nyu.edu', '2021-12-03 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 3', '2023-03-01', 300),
(9, 'user3@nyu.edu', '2022-07-04 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 3', '2023-03-01', 300),
(11, 'user3@nyu.edu', '2022-05-23 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 3', '2023-03-01', 300),
(12, 'testcustomer@nyu.edu', '2022-05-02 11:55:55', '1111-2222-3333-4444', 'Credit', 'Test Customer 1', '2023-03-01', 500),
(14, 'user3@nyu.edu', '2022-11-20 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 3', '2023-03-01', 400),
(15, 'user1@nyu.edu', '2022-11-21 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 1', '2023-03-01', 400),
(16, 'user2@nyu.edu', '2022-09-19 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 2', '2023-03-01', 800),
(17, 'user1@nyu.edu', '2022-08-11 11:55:55', '1111-2222-3333-5555', 'Credit', 'User 1', '2023-03-01', 300),
(18, 'testcustomer@nyu.edu', '2022-09-25 11:55:55', '1111-2222-3333-4444', 'Credit', 'Test Customer 1', '2023-03-01', 300),
(19, 'user1@nyu.edu', '2022-11-22 11:55:55', '1111-2222-3333-4444', 'Credit', 'Test Customer 1', '2023-03-01', 3000),
(20, 'testcustomer@nyu.edu', '2022-07-12 11:55:55', '1111-2222-3333-4444', 'Credit', 'Test Customer 1', '2023-03-01', 3000);

-- --------------------------------------------------------

--
-- Table structure for table `rate`
--

CREATE TABLE `rate` (
  `Rating` float NOT NULL,
  `Comment` varchar(1000) NOT NULL,
  `FlightNumber` varchar(50) NOT NULL,
  `DepartureDateandTime` datetime NOT NULL,
  `AirlineName` varchar(50) NOT NULL,
  `EmailAddress` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `rate`
--

INSERT INTO `rate` (`Rating`, `Comment`, `FlightNumber`, `DepartureDateandTime`, `AirlineName`, `EmailAddress`) VALUES
(4, 'Very Comfortable', '102', '2022-09-12 13:25:25', 'United', 'testcustomer@nyu.edu'),
(4, 'Relaxing, check-in and onboarding very professional', '102', '2022-09-12 13:25:25', 'United', 'user1@nyu.edu'),
(3, 'Satisfied and will use the same flight again', '102', '2022-09-12 13:25:25', 'United', 'user2@nyu.edu'),
(1, 'Customer Care services are not good', '104', '2022-10-04 13:25:25', 'United', 'testcustomer@nyu.edu'),
(4, 'Comfortable journey and Professional', '104', '2022-10-04 13:25:25', 'United', 'user1@nyu.edu');

-- --------------------------------------------------------

--
-- Table structure for table `staffemailaddress`
--

CREATE TABLE `staffemailaddress` (
  `Username` varchar(50) NOT NULL,
  `EmailAddress` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `staffemailaddress`
--

INSERT INTO `staffemailaddress` (`Username`, `EmailAddress`) VALUES
('admin', 'staff@nyu.edu'),
('jd123', 'hellow@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `staffphonenumber`
--

CREATE TABLE `staffphonenumber` (
  `Username` varchar(50) NOT NULL,
  `PhoneNumber` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `staffphonenumber`
--

INSERT INTO `staffphonenumber` (`Username`, `PhoneNumber`) VALUES
('admin', '111-2222-3333'),
('admin', '444-5555-6666'),
('jd123', '12345678');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `TicketIDNumber` int(11) NOT NULL,
  `FlightNumber` varchar(50) NOT NULL,
  `DepartureDateandTime` datetime NOT NULL,
  `AirlineName` varchar(50) NOT NULL,
  `Class` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`TicketIDNumber`, `FlightNumber`, `DepartureDateandTime`, `AirlineName`, `Class`) VALUES
(1, '102', '2022-09-12 13:25:25', 'United', 'Economy'),
(2, '102', '2022-09-12 13:25:25', 'United', 'Economy'),
(3, '102', '2022-09-12 13:25:25', 'United', 'Economy'),
(4, '104', '2022-10-04 13:25:25', 'United', 'Economy'),
(5, '104', '2022-10-04 13:25:25', 'United', 'Economy'),
(6, '106', '2022-08-04 13:25:25', 'United', 'Economy'),
(7, '106', '2022-08-04 13:25:25', 'United', 'Economy'),
(8, '839', '2021-12-26 13:25:25', 'United', 'Economy'),
(9, '102', '2022-09-12 13:25:25', 'United', 'Economy'),
(11, '134', '2022-07-12 13:25:25', 'United', 'Economy'),
(12, '715', '2022-09-28 10:25:25', 'United', 'Economy'),
(14, '206', '2023-02-04 13:25:25', 'United', 'Economy'),
(15, '206', '2023-02-04 13:25:25', 'United', 'Economy'),
(16, '206', '2023-02-04 13:25:25', 'United', 'Business'),
(17, '207', '2023-03-04 13:25:25', 'United', 'Economy'),
(18, '207', '2023-03-04 13:25:25', 'United', 'Economy'),
(19, '296', '2022-12-30 13:25:25', 'United', 'Economy'),
(20, '296', '2022-12-30 13:25:25', 'United', 'Economy');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`AirlineName`);

--
-- Indexes for table `airlinestaff`
--
ALTER TABLE `airlinestaff`
  ADD PRIMARY KEY (`Username`),
  ADD KEY `AirlineName` (`AirlineName`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`IDNumber`,`AirlineName`),
  ADD KEY `AirlineName` (`AirlineName`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`AirportName`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`EmailAddress`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`FlightNumber`,`DepartureDateandTime`,`AirlineName`),
  ADD KEY `DepartureAirportName` (`DepartureAirportName`),
  ADD KEY `ArrivalAirportName` (`ArrivalAirportName`),
  ADD KEY `IDNumber` (`IDNumber`,`AirlineName`),
  ADD KEY `AirlineName` (`AirlineName`);

--
-- Indexes for table `purchase`
--
ALTER TABLE `purchase`
  ADD PRIMARY KEY (`TicketIDNumber`),
  ADD KEY `EmailAddress` (`EmailAddress`);

--
-- Indexes for table `rate`
--
ALTER TABLE `rate`
  ADD PRIMARY KEY (`FlightNumber`,`DepartureDateandTime`,`AirlineName`,`EmailAddress`),
  ADD KEY `EmailAddress` (`EmailAddress`);

--
-- Indexes for table `staffemailaddress`
--
ALTER TABLE `staffemailaddress`
  ADD PRIMARY KEY (`Username`,`EmailAddress`);

--
-- Indexes for table `staffphonenumber`
--
ALTER TABLE `staffphonenumber`
  ADD PRIMARY KEY (`Username`,`PhoneNumber`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`TicketIDNumber`),
  ADD KEY `FlightNumber` (`FlightNumber`,`DepartureDateandTime`,`AirlineName`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airlinestaff`
--
ALTER TABLE `airlinestaff`
  ADD CONSTRAINT `airlinestaff_ibfk_1` FOREIGN KEY (`AirlineName`) REFERENCES `airline` (`AirlineName`) ON DELETE CASCADE;

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`AirlineName`) REFERENCES `airline` (`AirlineName`) ON DELETE CASCADE;

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`DepartureAirportName`) REFERENCES `airport` (`AirportName`) ON DELETE CASCADE,
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`ArrivalAirportName`) REFERENCES `airport` (`AirportName`) ON DELETE CASCADE,
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`IDNumber`,`AirlineName`) REFERENCES `airplane` (`IDNumber`, `AirlineName`) ON DELETE CASCADE,
  ADD CONSTRAINT `flight_ibfk_4` FOREIGN KEY (`AirlineName`) REFERENCES `airline` (`AirlineName`) ON DELETE CASCADE;

--
-- Constraints for table `purchase`
--
ALTER TABLE `purchase`
  ADD CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`TicketIDNumber`) REFERENCES `ticket` (`TicketIDNumber`) ON DELETE CASCADE,
  ADD CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`EmailAddress`) REFERENCES `customer` (`EmailAddress`) ON DELETE CASCADE;

--
-- Constraints for table `rate`
--
ALTER TABLE `rate`
  ADD CONSTRAINT `rate_ibfk_1` FOREIGN KEY (`FlightNumber`,`DepartureDateandTime`,`AirlineName`) REFERENCES `flight` (`FlightNumber`, `DepartureDateandTime`, `AirlineName`) ON DELETE CASCADE,
  ADD CONSTRAINT `rate_ibfk_2` FOREIGN KEY (`EmailAddress`) REFERENCES `customer` (`EmailAddress`) ON DELETE CASCADE;

--
-- Constraints for table `staffemailaddress`
--
ALTER TABLE `staffemailaddress`
  ADD CONSTRAINT `staffemailaddress_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `airlinestaff` (`Username`) ON DELETE CASCADE;

--
-- Constraints for table `staffphonenumber`
--
ALTER TABLE `staffphonenumber`
  ADD CONSTRAINT `staffphonenumber_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `airlinestaff` (`Username`) ON DELETE CASCADE;

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`FlightNumber`,`DepartureDateandTime`,`AirlineName`) REFERENCES `flight` (`FlightNumber`, `DepartureDateandTime`, `AirlineName`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
