-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 15, 2024 at 06:24 AM
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
-- Database: `gulf_oil_bd`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer_type`
--

CREATE TABLE `customer_type` (
  `id` int(11) NOT NULL,
  `cid` varchar(20) NOT NULL,
  `type` varchar(100) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `level_name_settings`
--

CREATE TABLE `level_name_settings` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `depth` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `starting_code` varchar(100) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `rep_client`
--

CREATE TABLE `rep_client` (
  `id` int(11) NOT NULL,
  `cid` varchar(100) DEFAULT '',
  `rep_id` varchar(100) DEFAULT '',
  `name` varchar(200) DEFAULT '',
  `client_id` varchar(200) DEFAULT '',
  `client_name` varchar(200) DEFAULT '',
  `field1` varchar(100) DEFAULT '',
  `field2` int(55) DEFAULT 0,
  `note` varchar(200) DEFAULT '',
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(100) DEFAULT '',
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(100) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sm_attendance`
--

CREATE TABLE `sm_attendance` (
  `id` int(11) NOT NULL,
  `cid` varchar(100) DEFAULT NULL,
  `rep_id` varchar(100) DEFAULT NULL,
  `rep_name` varchar(150) DEFAULT NULL,
  `user_type` varchar(100) DEFAULT NULL,
  `check_in_date` date DEFAULT NULL,
  `m_check_in` datetime DEFAULT NULL,
  `m_check_in_latlong` varchar(350) DEFAULT NULL,
  `m_check_out` datetime DEFAULT NULL,
  `m_check_out_latlong` varchar(350) DEFAULT NULL,
  `e_check_in` datetime DEFAULT NULL,
  `e_check_in_latlong` varchar(350) DEFAULT NULL,
  `e_check_out` datetime DEFAULT NULL,
  `e_check_out_latlong` varchar(350) DEFAULT NULL,
  `meter_reading_st` int(11) NOT NULL DEFAULT 0,
  `meter_reading_end` int(11) NOT NULL DEFAULT 0,
  `field1` varchar(300) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(200) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(200) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_cancel_reason`
--

CREATE TABLE `sm_cancel_reason` (
  `id` int(11) NOT NULL,
  `cid` varchar(512) DEFAULT NULL,
  `reason` varchar(512) DEFAULT NULL,
  `field1` varchar(512) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(512) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(512) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_category_type`
--

CREATE TABLE `sm_category_type` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `type_name` varchar(100) DEFAULT NULL,
  `cat_type_id` varchar(100) DEFAULT NULL,
  `cat_type_name` varchar(100) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_client`
--

CREATE TABLE `sm_client` (
  `id` int(11) NOT NULL,
  `cid` varchar(20) NOT NULL DEFAULT 'GULF',
  `client_id` varchar(20) NOT NULL DEFAULT '',
  `client_old_id` varchar(20) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  `area_id` varchar(20) NOT NULL DEFAULT '',
  `customer_type` varchar(100) DEFAULT '',
  `status` varchar(20) NOT NULL DEFAULT 'ACTIVE',
  `image_url` varchar(255) NOT NULL DEFAULT '',
  `token` varchar(255) NOT NULL DEFAULT '',
  `op_balance` double NOT NULL DEFAULT 0,
  `balance` double NOT NULL DEFAULT 0,
  `credit_limit` double NOT NULL DEFAULT 0,
  `credit_duration` int(11) NOT NULL DEFAULT 0,
  `payment_mode` varchar(10) NOT NULL DEFAULT '',
  `bank_account_no` varchar(50) NOT NULL DEFAULT '',
  `address` varchar(255) NOT NULL DEFAULT '',
  `latitude` varchar(100) NOT NULL DEFAULT '',
  `longitude` varchar(100) NOT NULL DEFAULT '',
  `submitted_by` varchar(200) DEFAULT '',
  `approved_by_sup` varchar(20) DEFAULT 'NO',
  `approval_status` varchar(200) DEFAULT '',
  `depot_id` varchar(10) NOT NULL DEFAULT '',
  `depot_name` varchar(100) NOT NULL DEFAULT '',
  `store_id` varchar(10) NOT NULL DEFAULT '',
  `store_name` varchar(100) NOT NULL DEFAULT '',
  `depot_belt_name` varchar(100) NOT NULL DEFAULT '',
  `category_id` varchar(50) NOT NULL DEFAULT '',
  `category_name` varchar(200) NOT NULL DEFAULT '',
  `sub_category_id` varchar(50) NOT NULL DEFAULT '',
  `sub_category_name` varchar(200) NOT NULL DEFAULT '',
  `market_id` varchar(20) NOT NULL DEFAULT '',
  `market_name` varchar(100) NOT NULL DEFAULT '',
  `owner_name` varchar(100) NOT NULL DEFAULT '',
  `nid` bigint(20) NOT NULL DEFAULT 0,
  `passport` varchar(100) NOT NULL DEFAULT '',
  `trade_license` varchar(20) NOT NULL DEFAULT '',
  `trade_license_no` varchar(100) NOT NULL DEFAULT '',
  `vat_registration` varchar(20) NOT NULL DEFAULT '',
  `vat_registration_no` varchar(100) NOT NULL DEFAULT '',
  `contact_no1` bigint(20) NOT NULL DEFAULT 0,
  `contact_no2` bigint(20) NOT NULL DEFAULT 0,
  `dob` date NOT NULL DEFAULT '1900-01-01',
  `dom` date NOT NULL DEFAULT '1900-01-01',
  `kids_info` varchar(100) NOT NULL DEFAULT '',
  `hobby` varchar(255) NOT NULL DEFAULT '',
  `manager_name` varchar(100) NOT NULL DEFAULT '',
  `manager_contact_no` bigint(20) NOT NULL DEFAULT 0,
  `starting_year` int(11) NOT NULL DEFAULT 0,
  `monthly_sales_capacity` int(11) NOT NULL DEFAULT 0,
  `monthly_sales` int(11) NOT NULL DEFAULT 0,
  `shop_owner_status` varchar(20) NOT NULL DEFAULT '',
  `warehouse_capacity` int(11) NOT NULL DEFAULT 0,
  `shop_size` int(11) NOT NULL DEFAULT 0,
  `shop_front_size` int(11) NOT NULL DEFAULT 0,
  `photo` varchar(100) NOT NULL DEFAULT '',
  `photo_str` varchar(100) NOT NULL DEFAULT '',
  `thana_id` int(11) NOT NULL DEFAULT 0,
  `thana` varchar(100) NOT NULL DEFAULT '',
  `district_id` varchar(50) NOT NULL DEFAULT '',
  `district` varchar(100) NOT NULL DEFAULT '',
  `field1` varchar(255) NOT NULL DEFAULT '',
  `field2` int(11) NOT NULL DEFAULT 0,
  `note` varchar(255) NOT NULL DEFAULT '',
  `created_on` datetime NOT NULL DEFAULT '1900-01-01 00:00:00',
  `created_by` varchar(30) NOT NULL DEFAULT '',
  `updated_on` datetime NOT NULL DEFAULT '1900-01-01 00:00:00',
  `updated_by` varchar(30) NOT NULL DEFAULT '',
  `approved_by_id` varchar(200) DEFAULT '',
  `approved_by_name` varchar(200) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_client_temp`
--

CREATE TABLE `sm_client_temp` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `client_id` varchar(20) DEFAULT NULL,
  `client_old_id` varchar(20) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `area_id` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `op_balance` double DEFAULT NULL,
  `balance` double DEFAULT NULL,
  `credit_limit` double DEFAULT NULL,
  `credit_duration` int(11) NOT NULL DEFAULT 0,
  `payment_mode` varchar(10) NOT NULL DEFAULT 'CASH',
  `bank_account_no` varchar(50) DEFAULT NULL,
  `no_of_doctor` int(11) NOT NULL DEFAULT 0,
  `avg_patient` int(11) NOT NULL DEFAULT 0,
  `has_drug_store` varchar(10) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `latitude` varchar(100) NOT NULL DEFAULT '0',
  `longitude` varchar(100) NOT NULL DEFAULT '0',
  `depot_id` varchar(10) DEFAULT NULL,
  `depot_name` varchar(100) DEFAULT NULL,
  `store_id` varchar(10) DEFAULT NULL,
  `store_name` varchar(100) DEFAULT NULL,
  `depot_belt_name` varchar(100) DEFAULT 'Default',
  `category_id` varchar(50) DEFAULT '11',
  `category_name` varchar(200) DEFAULT 'Retailer',
  `sub_category_id` varchar(50) DEFAULT '0',
  `sub_category_name` varchar(200) DEFAULT 'Not Applicable',
  `market_id` varchar(20) DEFAULT 'DEFAULT',
  `market_name` varchar(100) DEFAULT 'Default',
  `owner_name` varchar(100) DEFAULT NULL,
  `nid` bigint(20) DEFAULT NULL,
  `passport` varchar(100) NOT NULL DEFAULT '',
  `trade_license` varchar(20) NOT NULL DEFAULT '',
  `trade_license_no` varchar(100) NOT NULL DEFAULT '',
  `vat_registration` varchar(20) NOT NULL DEFAULT '',
  `vat_registration_no` varchar(100) NOT NULL DEFAULT '',
  `drug_registration_num` varchar(100) DEFAULT '0',
  `doctor` varchar(20) DEFAULT NULL,
  `contact_no1` bigint(20) DEFAULT NULL,
  `contact_no2` bigint(20) DEFAULT NULL,
  `dob` date DEFAULT '1900-01-01',
  `dom` date DEFAULT '1900-01-01',
  `kids_info` varchar(100) NOT NULL DEFAULT '',
  `hobby` varchar(255) NOT NULL DEFAULT '',
  `manager_name` varchar(100) NOT NULL DEFAULT '',
  `manager_contact_no` bigint(20) DEFAULT NULL,
  `starting_year` int(11) DEFAULT 0,
  `monthly_sales_capacity` int(11) DEFAULT NULL,
  `monthly_sales` int(11) DEFAULT NULL,
  `shop_owner_status` varchar(20) NOT NULL DEFAULT '',
  `warehouse_capacity` int(11) DEFAULT NULL,
  `shop_size` int(11) DEFAULT NULL,
  `shop_front_size` int(11) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `photo_str` varchar(100) NOT NULL DEFAULT '',
  `thana_id` int(11) DEFAULT 0,
  `thana` varchar(100) DEFAULT 'Default',
  `district_id` varchar(50) DEFAULT '0',
  `district` varchar(100) DEFAULT 'Default',
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT 0,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT '1900-01-01 00:00:00',
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT '1900-01-01 00:00:00',
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_company_settings`
--

CREATE TABLE `sm_company_settings` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `http_pass` varchar(20) DEFAULT NULL,
  `subscription_model` varchar(20) DEFAULT NULL,
  `clean_Data` varchar(20) DEFAULT NULL,
  `keep_history` varchar(20) DEFAULT NULL,
  `subscription_date` date DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `admin_mobile_no` varchar(20) DEFAULT NULL,
  `item_list` longtext DEFAULT NULL,
  `item_list_mobile` longtext DEFAULT NULL,
  `temp_item_list` longtext DEFAULT NULL,
  `field1` longtext DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_inbox`
--

CREATE TABLE `sm_inbox` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `sl` int(11) DEFAULT NULL,
  `mobile_no` varchar(20) DEFAULT NULL,
  `sms_date` datetime DEFAULT NULL,
  `sms` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `error_in_sms` varchar(255) DEFAULT NULL,
  `ho_status` int(11) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_item`
--

CREATE TABLE `sm_item` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `item_id` varchar(20) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `pack_size` varchar(150) NOT NULL DEFAULT '',
  `des` varchar(255) DEFAULT NULL,
  `category_id` varchar(20) DEFAULT NULL,
  `category_id_sp` varchar(20) DEFAULT NULL,
  `unit_type` varchar(20) DEFAULT NULL,
  `manufacturer` varchar(50) DEFAULT NULL,
  `item_carton` int(11) NOT NULL DEFAULT 0,
  `price` double DEFAULT NULL,
  `dist_price` double NOT NULL DEFAULT 0,
  `vat_amt` double NOT NULL DEFAULT 0,
  `total_amt` double NOT NULL DEFAULT 0,
  `status` varchar(20) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_level`
--

CREATE TABLE `sm_level` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `level_id` varchar(20) DEFAULT NULL,
  `level_name` varchar(100) DEFAULT NULL,
  `parent_level_id` varchar(20) DEFAULT NULL,
  `parent_level_name` varchar(100) DEFAULT NULL,
  `is_leaf` varchar(20) DEFAULT NULL,
  `area_id_list` varchar(255) DEFAULT NULL,
  `special_territory_code` varchar(20) NOT NULL DEFAULT '-',
  `depot_id` varchar(20) DEFAULT NULL,
  `depth` int(11) DEFAULT NULL,
  `level0` varchar(20) DEFAULT NULL,
  `level0_name` varchar(100) DEFAULT NULL,
  `level1` varchar(20) DEFAULT NULL,
  `level1_name` varchar(100) DEFAULT NULL,
  `level2` varchar(20) DEFAULT NULL,
  `level2_name` varchar(100) DEFAULT NULL,
  `level3` varchar(20) DEFAULT NULL,
  `level3_name` varchar(100) DEFAULT NULL,
  `level4` varchar(20) DEFAULT NULL,
  `level4_name` varchar(100) DEFAULT NULL,
  `level5` varchar(20) DEFAULT NULL,
  `level5_name` varchar(100) DEFAULT NULL,
  `level6` varchar(20) DEFAULT NULL,
  `level6_name` varchar(100) DEFAULT NULL,
  `level7` varchar(20) DEFAULT NULL,
  `level7_name` varchar(100) DEFAULT NULL,
  `level8` varchar(20) DEFAULT NULL,
  `level8_name` varchar(100) DEFAULT NULL,
  `territory_des` varchar(100) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_linkpath`
--

CREATE TABLE `sm_linkpath` (
  `id` int(11) NOT NULL,
  `cid` varchar(100) NOT NULL DEFAULT 'GULF',
  `link_name` varchar(100) DEFAULT '',
  `link_path` varchar(255) DEFAULT '',
  `user_type` varchar(100) DEFAULT '',
  `field1` varchar(100) DEFAULT '',
  `field2` int(11) DEFAULT 0,
  `note` varchar(200) DEFAULT '',
  `created_on` datetime DEFAULT current_timestamp(),
  `created_by` varchar(100) DEFAULT '',
  `updated_on` datetime DEFAULT current_timestamp(),
  `updated_by` varchar(100) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_mobile_settings`
--

CREATE TABLE `sm_mobile_settings` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `sl` int(11) DEFAULT NULL,
  `s_key` varchar(20) DEFAULT NULL,
  `s_value` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_mobile_settings_pharma`
--

CREATE TABLE `sm_mobile_settings_pharma` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `sl` int(11) DEFAULT NULL,
  `s_key` varchar(50) DEFAULT NULL,
  `s_value` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_order`
--

CREATE TABLE `sm_order` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT 'GULF',
  `vsl` int(11) DEFAULT 0,
  `depot_id` varchar(10) DEFAULT '',
  `depot_name` varchar(100) DEFAULT '',
  `sl` int(11) DEFAULT 0,
  `store_id` varchar(10) DEFAULT '',
  `store_name` varchar(100) DEFAULT '',
  `client_id` varchar(20) DEFAULT '',
  `client_name` varchar(100) DEFAULT '',
  `rep_id` varchar(20) DEFAULT '',
  `rep_name` varchar(100) DEFAULT '',
  `market_id` varchar(20) DEFAULT '',
  `market_name` varchar(100) DEFAULT '',
  `order_date` date DEFAULT '1990-01-01',
  `order_datetime` datetime DEFAULT '1990-01-01 00:00:00',
  `delivery_date` date DEFAULT '1990-01-01',
  `collection_date` date DEFAULT '1990-01-01',
  `payment_mode` varchar(20) DEFAULT '',
  `area_id` varchar(20) DEFAULT '',
  `area_name` varchar(100) DEFAULT '',
  `level0_id` varchar(20) DEFAULT '',
  `level0_name` varchar(100) DEFAULT '',
  `level1_id` varchar(20) DEFAULT '',
  `level1_name` varchar(100) DEFAULT '',
  `level2_id` varchar(20) DEFAULT '',
  `level2_name` varchar(100) DEFAULT '',
  `level3_id` varchar(20) DEFAULT '',
  `level3_name` varchar(100) DEFAULT '',
  `status` varchar(20) DEFAULT '',
  `invoice_ref` int(11) DEFAULT 0,
  `item_id` varchar(20) DEFAULT '',
  `item_name` varchar(100) DEFAULT '',
  `category_id` varchar(20) DEFAULT '',
  `category_id_sp` varchar(100) DEFAULT '',
  `quantity` int(11) DEFAULT 0,
  `price` double DEFAULT 0,
  `item_vat` double DEFAULT 0,
  `item_unit` varchar(20) DEFAULT '',
  `item_carton` int(11) DEFAULT 0,
  `total_price` double DEFAULT 0,
  `order_media` varchar(20) DEFAULT '',
  `device_user_agent` varchar(50) DEFAULT '',
  `ip_ref` varchar(50) DEFAULT '',
  `ym_date` date DEFAULT '1990-01-01',
  `depot_status` varchar(2) DEFAULT '',
  `ho_status` varchar(2) DEFAULT '',
  `flag_depot_stock` int(2) DEFAULT 0,
  `flag_data` varchar(2) DEFAULT '',
  `field1` varchar(255) DEFAULT '',
  `field2` int(11) DEFAULT 0,
  `note` varchar(255) DEFAULT '',
  `created_on` datetime DEFAULT '1990-01-01 00:00:00',
  `created_by` varchar(30) DEFAULT '',
  `updated_on` datetime DEFAULT '1990-01-01 00:00:00',
  `updated_by` varchar(30) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sm_order_head`
--

CREATE TABLE `sm_order_head` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT 'GULF',
  `depot_id` varchar(10) DEFAULT '',
  `depot_name` varchar(100) DEFAULT '',
  `sl` int(11) DEFAULT 0,
  `store_id` varchar(10) DEFAULT '',
  `store_name` varchar(100) DEFAULT '',
  `client_id` varchar(20) DEFAULT '',
  `client_name` varchar(100) DEFAULT '',
  `rep_id` varchar(20) DEFAULT '',
  `rep_name` varchar(100) DEFAULT '',
  `market_id` varchar(20) DEFAULT '',
  `market_name` varchar(100) DEFAULT '',
  `order_date` date DEFAULT '1990-01-01',
  `order_datetime` datetime DEFAULT '1990-01-01 00:00:00',
  `delivery_date` date DEFAULT '1990-01-01',
  `collection_date` date DEFAULT '1990-01-01',
  `payment_mode` varchar(20) DEFAULT '',
  `area_id` varchar(20) DEFAULT '',
  `area_name` varchar(100) DEFAULT '',
  `level0_id` varchar(20) DEFAULT '',
  `level0_name` varchar(100) DEFAULT '',
  `level1_id` varchar(20) DEFAULT '',
  `level1_name` varchar(100) DEFAULT '',
  `level2_id` varchar(20) DEFAULT '',
  `level2_name` varchar(100) DEFAULT '',
  `level3_id` varchar(20) DEFAULT '',
  `level3_name` varchar(100) DEFAULT '',
  `status` varchar(20) DEFAULT '',
  `invoice_ref` int(11) DEFAULT 0,
  `order_media` varchar(20) DEFAULT '',
  `device_user_agent` varchar(50) DEFAULT '',
  `ip_ref` varchar(50) DEFAULT '',
  `ym_date` date DEFAULT '1990-01-01',
  `depot_status` varchar(2) DEFAULT '',
  `ho_status` varchar(2) DEFAULT '',
  `flag_depot_stock` int(2) DEFAULT 0,
  `flag_data` varchar(2) DEFAULT '',
  `visit_type` varchar(50) DEFAULT '',
  `user_type` varchar(20) DEFAULT '',
  `mobile_no` varchar(20) DEFAULT '',
  `client_cat` varchar(20) DEFAULT '',
  `start_time` datetime DEFAULT '1990-01-01 00:00:00',
  `end_time` datetime DEFAULT '1990-01-01 00:00:00',
  `lat_long` varchar(50) DEFAULT '',
  `location_detail` varchar(50) DEFAULT '',
  `last_location` varchar(10) DEFAULT '',
  `visit_image` varchar(100) DEFAULT '',
  `promo_ref` int(2) DEFAULT 0,
  `r_flag` int(2) DEFAULT 0,
  `field1` varchar(255) DEFAULT '',
  `field2` int(11) DEFAULT 0,
  `note` varchar(255) DEFAULT '',
  `created_on` datetime DEFAULT '1990-01-01 00:00:00',
  `created_by` varchar(30) DEFAULT '',
  `updated_on` datetime DEFAULT '1990-01-01 00:00:00',
  `updated_by` varchar(30) DEFAULT '',
  `total_price` double DEFAULT 0,
  `order_info` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_paytype`
--

CREATE TABLE `sm_paytype` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `paytype` varchar(20) DEFAULT NULL,
  `detail` varchar(255) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_rep`
--

CREATE TABLE `sm_rep` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `rep_id` varchar(20) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `mobile_no` varchar(20) DEFAULT NULL,
  `designation` varchar(100) DEFAULT '',
  `password` varchar(32) DEFAULT NULL,
  `token` varchar(200) NOT NULL DEFAULT '',
  `status` varchar(20) DEFAULT 'ACTIVE',
  `mac_address` varchar(100) DEFAULT NULL,
  `sync_code` varchar(20) DEFAULT NULL,
  `sync_code_servey` varchar(100) DEFAULT NULL,
  `sync_count` int(11) DEFAULT NULL,
  `first_sync_date` datetime DEFAULT NULL,
  `last_sync_date` datetime DEFAULT NULL,
  `monthly_sms_count` int(11) DEFAULT NULL,
  `monthly_voucher_count` int(11) DEFAULT NULL,
  `java` varchar(20) DEFAULT NULL,
  `wap` varchar(20) DEFAULT NULL,
  `android` varchar(20) DEFAULT NULL,
  `sms` varchar(255) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT NULL,
  `level_id` varchar(20) DEFAULT NULL,
  `depot_id` varchar(20) DEFAULT NULL,
  `sync_req_time` datetime DEFAULT NULL,
  `sync_flag` varchar(255) DEFAULT NULL,
  `sync_data` varchar(255) DEFAULT NULL,
  `version_number` varchar(100) DEFAULT '',
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL,
  `vehicle_no` varchar(20) NOT NULL,
  `meter_reading` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_rep_area`
--

CREATE TABLE `sm_rep_area` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `rep_id` varchar(20) DEFAULT NULL,
  `rep_name` varchar(100) DEFAULT NULL,
  `rep_category` varchar(20) DEFAULT NULL,
  `area_id` varchar(20) DEFAULT NULL,
  `area_name` varchar(100) DEFAULT NULL,
  `token` varchar(255) NOT NULL,
  `depot_id` varchar(20) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT current_timestamp(),
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT current_timestamp(),
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_roletask`
--

CREATE TABLE `sm_roletask` (
  `id` int(11) NOT NULL,
  `cid` varchar(20) DEFAULT NULL,
  `roleid` varchar(50) DEFAULT NULL,
  `taskid` varchar(50) DEFAULT NULL,
  `field1` varchar(50) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(50) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(50) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_settings`
--

CREATE TABLE `sm_settings` (
  `id` int(11) NOT NULL,
  `cid` varchar(20) DEFAULT NULL,
  `s_key` varchar(100) DEFAULT NULL,
  `s_value` varchar(100) DEFAULT NULL,
  `activity_id_list` longtext DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_settings_pharma`
--

CREATE TABLE `sm_settings_pharma` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `s_key` varchar(50) DEFAULT NULL,
  `s_value` varchar(50) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_supervisor_level`
--

CREATE TABLE `sm_supervisor_level` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) DEFAULT NULL,
  `sup_id` varchar(20) DEFAULT NULL,
  `sup_name` varchar(100) DEFAULT NULL,
  `level_id` varchar(20) DEFAULT NULL,
  `level_name` varchar(100) DEFAULT NULL,
  `level_depth_no` int(11) DEFAULT NULL,
  `field1` varchar(255) DEFAULT NULL,
  `field2` int(11) DEFAULT NULL,
  `note` varchar(255) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `created_by` varchar(30) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `sm_tracking_live2`
--

CREATE TABLE `sm_tracking_live2` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) NOT NULL,
  `rep_id` varchar(20) NOT NULL DEFAULT '',
  `rep_name` varchar(100) NOT NULL,
  `region_id` varchar(20) DEFAULT '',
  `region_name` varchar(100) DEFAULT '',
  `zone_id` varchar(20) DEFAULT '',
  `zone_name` varchar(100) DEFAULT '',
  `area_id` varchar(20) DEFAULT '',
  `area_name` varchar(100) DEFAULT '',
  `territory_id` varchar(20) DEFAULT '',
  `territory_name` varchar(200) NOT NULL DEFAULT '-',
  `call_type` varchar(20) NOT NULL DEFAULT '',
  `visited_to_id` varchar(20) DEFAULT '',
  `visited_to_name` varchar(100) DEFAULT '',
  `visited_latlong` varchar(100) NOT NULL DEFAULT '0.0',
  `distance_km` int(11) NOT NULL DEFAULT 0,
  `distance_km_flag` int(1) NOT NULL DEFAULT 0,
  `visit_date` date NOT NULL DEFAULT '1900-01-01',
  `visit_time` varchar(100) NOT NULL DEFAULT '',
  `location_detail` varchar(100) NOT NULL DEFAULT '-'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sm_tracking_table`
--

CREATE TABLE `sm_tracking_table` (
  `id` int(11) NOT NULL,
  `cid` varchar(10) NOT NULL,
  `depot_id` varchar(10) NOT NULL,
  `depot_name` varchar(100) NOT NULL DEFAULT '',
  `area_id` varchar(20) NOT NULL,
  `area_name` varchar(100) NOT NULL,
  `sl` int(11) NOT NULL,
  `rep_id` varchar(20) NOT NULL DEFAULT '',
  `rep_name` varchar(100) NOT NULL,
  `call_type` varchar(20) NOT NULL DEFAULT '',
  `visited_id` varchar(20) NOT NULL DEFAULT '',
  `visited_name` varchar(100) NOT NULL DEFAULT '',
  `visited_latlong` varchar(100) NOT NULL DEFAULT '0.0',
  `actual_latlong` varchar(100) NOT NULL DEFAULT '0,0',
  `visit_type` varchar(20) NOT NULL DEFAULT '',
  `visit_date` date NOT NULL,
  `visit_time` varchar(100) NOT NULL DEFAULT '',
  `location_detail` varchar(100) NOT NULL DEFAULT '-',
  `last_location` varchar(10) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sm_user`
--

CREATE TABLE `sm_user` (
  `id` int(11) NOT NULL,
  `cid` varchar(20) DEFAULT NULL,
  `user_id` varchar(50) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `mobile` bigint(20) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `email_notification` varchar(10) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT NULL,
  `user_role` varchar(20) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `sync_code` int(11) DEFAULT NULL,
  `updated_on` datetime DEFAULT NULL,
  `updated_by` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `user_id` varchar(512) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customer_type`
--
ALTER TABLE `customer_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `level_name_settings`
--
ALTER TABLE `level_name_settings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `i1` (`cid`);

--
-- Indexes for table `rep_client`
--
ALTER TABLE `rep_client`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_attendance`
--
ALTER TABLE `sm_attendance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `meter_reading` (`cid`,`rep_id`,`check_in_date`,`note`);

--
-- Indexes for table `sm_cancel_reason`
--
ALTER TABLE `sm_cancel_reason`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_category_type`
--
ALTER TABLE `sm_category_type`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cid_typename` (`cid`,`type_name`),
  ADD KEY `cat_type_index` (`cid`,`cat_type_id`,`type_name`);

--
-- Indexes for table `sm_client`
--
ALTER TABLE `sm_client`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_client_temp`
--
ALTER TABLE `sm_client_temp`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_company_settings`
--
ALTER TABLE `sm_company_settings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `i1` (`cid`,`status`);

--
-- Indexes for table `sm_inbox`
--
ALTER TABLE `sm_inbox`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_item`
--
ALTER TABLE `sm_item`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cid_itemid` (`cid`,`item_id`);

--
-- Indexes for table `sm_level`
--
ALTER TABLE `sm_level`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cid_levelid_isleaf` (`cid`,`level_id`,`is_leaf`),
  ADD KEY `l2` (`cid`,`level_id`),
  ADD KEY `i3` (`cid`,`is_leaf`,`special_territory_code`),
  ADD KEY `i4` (`is_leaf`),
  ADD KEY `level0` (`level0`),
  ADD KEY `level0_2` (`level0`,`level1`),
  ADD KEY `level0_3` (`level0`,`level1`,`level2`),
  ADD KEY `level0_4` (`level0`,`level1`,`level2`,`level3`),
  ADD KEY `cid` (`cid`,`depth`),
  ADD KEY `r1` (`cid`,`level1`),
  ADD KEY `r2` (`cid`,`level2`),
  ADD KEY `rn1` (`cid`,`level_id`),
  ADD KEY `sr2` (`cid`,`is_leaf`,`depth`),
  ADD KEY `a1` (`cid`,`depth`);

--
-- Indexes for table `sm_linkpath`
--
ALTER TABLE `sm_linkpath`
  ADD PRIMARY KEY (`id`),
  ADD KEY `s1` (`cid`,`user_type`);

--
-- Indexes for table `sm_mobile_settings`
--
ALTER TABLE `sm_mobile_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_mobile_settings_pharma`
--
ALTER TABLE `sm_mobile_settings_pharma`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_order`
--
ALTER TABLE `sm_order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cid_vsl` (`cid`,`vsl`),
  ADD KEY `cid_areaid` (`cid`),
  ADD KEY `i1` (`cid`,`sl`,`rep_id`,`delivery_date`,`area_id`),
  ADD KEY `i2` (`sl`),
  ADD KEY `i3` (`cid`,`client_id`),
  ADD KEY `i4` (`cid`,`rep_id`,`delivery_date`,`area_id`),
  ADD KEY `i5` (`cid`,`client_id`,`sl`),
  ADD KEY `i6` (`area_id`),
  ADD KEY `i7` (`vsl`),
  ADD KEY `rep_id` (`rep_id`),
  ADD KEY `vsl_repid` (`vsl`,`rep_id`),
  ADD KEY `C1` (`cid`,`order_date`),
  ADD KEY `C2` (`client_id`,`area_id`),
  ADD KEY `cid` (`cid`,`order_date`);

--
-- Indexes for table `sm_order_head`
--
ALTER TABLE `sm_order_head`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `depoid_sl` (`cid`,`depot_id`,`sl`),
  ADD KEY `cid_depotid_sl_storeid_areaid` (`cid`,`depot_id`,`sl`,`store_id`,`area_id`),
  ADD KEY `o1` (`order_datetime`,`ho_status`),
  ADD KEY `02` (`cid`,`order_date`),
  ADD KEY `q1` (`cid`,`delivery_date`),
  ADD KEY `cid` (`cid`,`rep_id`,`client_id`),
  ADD KEY `i10` (`cid`,`rep_id`,`client_id`),
  ADD KEY `i11` (`cid`,`client_id`),
  ADD KEY `i12` (`sl`),
  ADD KEY `i13` (`cid`,`rep_id`,`delivery_date`,`field1`),
  ADD KEY `cid_2` (`cid`,`order_date`),
  ADD KEY `ho_stat` (`cid`,`ho_status`),
  ADD KEY `sr1` (`order_date`,`client_id`),
  ADD KEY `i19` (`order_date`,`area_id`),
  ADD KEY `r1` (`cid`,`order_date`,`area_id`),
  ADD KEY `r2` (`cid`,`order_date`,`level2_id`),
  ADD KEY `r3` (`cid`,`order_date`,`level2_id`,`area_id`),
  ADD KEY `r111` (`cid`,`order_date`);

--
-- Indexes for table `sm_paytype`
--
ALTER TABLE `sm_paytype`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_rep`
--
ALTER TABLE `sm_rep`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cid_repid` (`cid`,`rep_id`),
  ADD KEY `i1` (`rep_id`),
  ADD KEY `i2` (`cid`,`rep_id`,`password`,`sync_code`,`status`),
  ADD KEY `note` (`note`),
  ADD KEY `dw` (`cid`,`user_type`,`note`),
  ADD KEY `d3` (`cid`,`note`);

--
-- Indexes for table `sm_rep_area`
--
ALTER TABLE `sm_rep_area`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cid_repid_areaid` (`cid`,`rep_id`,`area_id`),
  ADD KEY `i1` (`cid`,`rep_id`),
  ADD KEY `i2` (`cid`),
  ADD KEY `area_id` (`area_id`);

--
-- Indexes for table `sm_roletask`
--
ALTER TABLE `sm_roletask`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_settings`
--
ALTER TABLE `sm_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sm_settings_pharma`
--
ALTER TABLE `sm_settings_pharma`
  ADD PRIMARY KEY (`id`),
  ADD KEY `i1` (`cid`,`s_key`);

--
-- Indexes for table `sm_supervisor_level`
--
ALTER TABLE `sm_supervisor_level`
  ADD PRIMARY KEY (`id`),
  ADD KEY `i1` (`cid`,`sup_id`),
  ADD KEY `r1` (`cid`,`level_id`),
  ADD KEY `rank1` (`cid`,`level_depth_no`,`level_id`),
  ADD KEY `r2` (`cid`,`level_depth_no`,`level_id`,`sup_id`);

--
-- Indexes for table `sm_tracking_live2`
--
ALTER TABLE `sm_tracking_live2`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rep_id` (`rep_id`),
  ADD KEY `cid` (`cid`,`rep_id`),
  ADD KEY `dist01` (`cid`,`visit_date`),
  ADD KEY `d2` (`cid`,`rep_id`,`visit_date`),
  ADD KEY `pr1` (`cid`);

--
-- Indexes for table `sm_tracking_table`
--
ALTER TABLE `sm_tracking_table`
  ADD PRIMARY KEY (`id`),
  ADD KEY `visit_date` (`visit_date`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customer_type`
--
ALTER TABLE `customer_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `level_name_settings`
--
ALTER TABLE `level_name_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `rep_client`
--
ALTER TABLE `rep_client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_attendance`
--
ALTER TABLE `sm_attendance`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_category_type`
--
ALTER TABLE `sm_category_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_client`
--
ALTER TABLE `sm_client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_company_settings`
--
ALTER TABLE `sm_company_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_item`
--
ALTER TABLE `sm_item`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_level`
--
ALTER TABLE `sm_level`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_linkpath`
--
ALTER TABLE `sm_linkpath`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_mobile_settings`
--
ALTER TABLE `sm_mobile_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_order`
--
ALTER TABLE `sm_order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_order_head`
--
ALTER TABLE `sm_order_head`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_paytype`
--
ALTER TABLE `sm_paytype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_rep`
--
ALTER TABLE `sm_rep`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_rep_area`
--
ALTER TABLE `sm_rep_area`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_settings`
--
ALTER TABLE `sm_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_settings_pharma`
--
ALTER TABLE `sm_settings_pharma`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_supervisor_level`
--
ALTER TABLE `sm_supervisor_level`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_tracking_live2`
--
ALTER TABLE `sm_tracking_live2`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sm_tracking_table`
--
ALTER TABLE `sm_tracking_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
