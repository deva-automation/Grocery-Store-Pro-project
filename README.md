# 🛒 FreshMart Pro - FastAPI E-commerce/Grocery Store

A complete, responsive, and master-level full-stack grocery store web application built with **FastAPI**, **SQLite**, **Jinja2**, and **Tailwind CSS**. This project demonstrates advanced backend logic, database management, and a dynamic frontend.

## 🚀 Features

* **Auto-Seeding Database:** Automatically populates the database with 12 dummy grocery items upon the first run.
* **Bilingual Support (EN/BN):** Dynamic Language Toggle (English & Bengali) using a custom string parser without refreshing the page.
* **Real-time Live Search:** Filter products instantly using the dynamic search bar.
* **Smart Cart & Checkout:** Add products to the cart, calculate total bills, and place orders seamlessly.
* **Inventory & Stock Management:** Real-time stock deduction upon successful order placement. Prevents ordering out-of-stock items.
* **Order History Tracking:** Customers can view their past orders, total bills, and purchased items by searching with their phone number.
* **Admin Panel:** A dedicated dashboard (`/admin`) to add new products, dual-language names, units, stock limits, and prices.

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy
* **Database:** SQLite
* **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript, FontAwesome
* **Template Engine:** Jinja2

## ⚙️ Installation & Setup

Follow these steps to run the project on your local machine:

**1. Clone the repository:**
```bash
git clone [https://github.com/YourUsername/FreshMart-FastAPI.git](https://github.com/YourUsername/FreshMart-FastAPI.git)
cd FreshMart-FastAPI
