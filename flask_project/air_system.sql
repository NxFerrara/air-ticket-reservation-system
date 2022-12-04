-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 04, 2022 at 08:31 PM
-- Server version: 5.7.34
-- PHP Version: 7.4.21

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
('American Airlines'),
('Delta'),
('Jet Blue');

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
('jd123', '1234567', 'Sally', 'Smith', '1980-11-11', 'Jet Blue'),
('nwill123', 'ilovechips', 'Nick', 'Williams', '2001-10-03', 'Jet Blue');

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
(1, 0, 'Boeing', 1, 'Jet Blue', 50, 20, 10),
(2, 0, 'Boeing', 3, 'Jet Blue', 70, 20, 10),
(3, 0, 'Boeing', 4, 'Jet Blue', 60, 40, 20);

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
('JFK', 'NYC', 'USA', 'Domestic'),
('PVG', 'Shanghai', 'China', 'International');

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
('Johnny Liu', 'batman@gmail.com', '1234', 145, 'Elm Street', 'New York', 'NY', '9241233478', 391238, '2027-01-08', 'USA', '2001-10-03'),
('Jason Rodriguez', 'jasonrodriguez@gmail.com', 'iwanttotravel', 298, 'Century Avenue', 'Pudong', 'Shanghai', '2168881234', 9281394, '2024-02-19', 'China', '1969-04-17'),
('John Doe', 'johndoe@gmail.com', 'ilovedatabases', 123, 'Maple Street', 'Los Angeles', 'CA', '7182911230', 3004786, '2022-12-21', 'USA', '1979-11-04'),
('Mary Jane', 'maryjane@gmail.com', 'ilikehamburgers', 652, 'Oak Street', 'New York', 'NY', '9172309482', 2391039, '2023-03-12', 'USA', '1989-06-15'),
('Max Chen', 'spiderman@gmail.com', '1234567', 301, 'Elk Street', 'Brooklyn', 'NY', '9281920394', 3928192, '2025-10-15', 'USA', '1956-02-10'),
('Sarah Thompson', 'sthompson@gmail.com', 'ilovefish', 341, 'Pine Street', 'Bronx', 'NY', '7182910394', 983712, '2028-10-18', 'USA', '2010-01-05');

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
('1', '2008-11-11 13:30:00', '2008-11-11 17:00:00', 100, 'On-time', 'JFK', 'PVG', 1, 'Jet Blue'),
('2', '2008-11-12 20:30:00', '2008-11-13 01:00:00', 200, 'Delayed', 'JFK', 'PVG', 3, 'Jet Blue'),
('3', '2008-12-11 01:00:00', '2008-12-11 05:30:00', 120, 'On-time', 'JFK', 'PVG', 1, 'Jet Blue'),
('4', '2009-01-20 04:00:00', '2009-01-20 09:30:00', 320, 'Delayed', 'JFK', 'PVG', 2, 'Jet Blue'),
('5', '2009-04-22 09:00:00', '2009-04-22 12:30:00', 90, 'On-time', 'JFK', 'PVG', 3, 'Jet Blue'),
('6', '2009-08-30 12:00:00', '2009-08-30 17:30:00', 180, 'Delayed', 'JFK', 'PVG', 2, 'Jet Blue'),
('7', '2023-08-30 13:30:00', '2023-08-30 19:00:00', 220, 'Delayed', 'JFK', 'PVG', 1, 'Jet Blue');

-- --------------------------------------------------------

--
-- Table structure for table `purchase`
--

CREATE TABLE `purchase` (
  `TicketIDNumber` varchar(50) NOT NULL,
  `EmailAddress` varchar(50) NOT NULL,
  `PurchaseDateandTime` datetime NOT NULL,
  `CardNumber` int(11) NOT NULL,
  `CardType` varchar(50) NOT NULL,
  `NameonCard` varchar(50) NOT NULL,
  `ExpirationDate` date NOT NULL,
  `sold_price` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`TicketIDNumber`, `EmailAddress`, `PurchaseDateandTime`, `CardNumber`, `CardType`, `NameonCard`, `ExpirationDate`, `sold_price`) VALUES
('1356', 'johndoe@gmail.com', '2008-11-08 13:27:00', 19283912, 'credit', 'John Doe', '2011-08-09', 200.53),
('2417', 'johndoe@gmail.com', '2008-11-09 09:56:00', 19283912, 'credit', 'John Doe', '2011-08-09', 378.19),
('3182', 'maryjane@gmail.com', '2008-12-02 21:13:00', 21938110, 'debit', 'Mary Jane', '2014-11-26', 401.02),
('3976', 'maryjane@gmail.com', '2008-12-03 07:30:00', 21938110, 'debit', 'Mary Jane', '2014-11-26', 403.56),
('4019', 'jasonrodriguez@gmail.com', '2009-01-15 12:46:00', 54102918, 'credit', 'Jason Rodriguez', '2016-05-27', 550.19),
('5108', 'jasonrodriguez@gmail.com', '2009-03-01 22:16:00', 54102918, 'credit', 'Jason Rodriguez', '2016-05-27', 165.18),
('7129', 'johndoe@gmail.com', '2022-11-04 15:19:00', 10293145, 'debit', 'John Doe', '2026-12-12', 389.46);

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
('jd123', 'ss123@gmail.com');

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
('jd123', '732-890-1667');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `TicketIDNumber` varchar(50) NOT NULL,
  `FlightNumber` varchar(50) NOT NULL,
  `DepartureDateandTime` datetime NOT NULL,
  `AirlineName` varchar(50) NOT NULL,
  `Class` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`TicketIDNumber`, `FlightNumber`, `DepartureDateandTime`, `AirlineName`, `Class`) VALUES
('1248', '1', '2008-11-11 13:30:00', 'Jet Blue', 'Economy'),
('1356', '1', '2008-11-11 13:30:00', 'Jet Blue', 'Economy'),
('2198', '2', '2008-11-12 20:30:00', 'Jet Blue', 'Business'),
('2417', '2', '2008-11-12 20:30:00', 'Jet Blue', 'Business'),
('3182', '3', '2008-12-11 01:00:00', 'Jet Blue', 'Business'),
('3976', '3', '2008-12-11 01:00:00', 'Jet Blue', 'Economy'),
('4019', '4', '2009-01-20 04:00:00', 'Jet Blue', 'Economy'),
('4192', '4', '2009-01-20 04:00:00', 'Jet Blue', 'Economy'),
('5108', '5', '2009-04-22 09:00:00', 'Jet Blue', 'First'),
('5768', '5', '2009-04-22 09:00:00', 'Jet Blue', 'First'),
('6123', '6', '2009-08-30 12:00:00', 'Jet Blue', 'First'),
('6527', '6', '2009-08-30 12:00:00', 'Jet Blue', 'First'),
('7129', '7', '2023-08-30 13:30:00', 'Jet Blue', 'Economy'),
('7891', '7', '2023-08-30 13:30:00', 'Jet Blue', 'Business');

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
