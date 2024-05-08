

---

# Vendor Management System

This project is a Vendor Management System developed using Django and Django REST Framework. It allows for the management of vendor profiles, tracking of purchase orders, and calculation of vendor performance metrics.

## Installation

### Installing Pipenv

#### Using pip (Python Package Installer)

If you have Python and pip installed, you can use pip to install Pipenv globally:

```bash
pip install pipenv
```

#### Using Homebrew (macOS and Linux)

If you're on macOS or Linux, you can install Pipenv using Homebrew:

```bash
brew install pipenv
```

### Setting Up the Project

1. Clone the repository:

    ```bash
    git clone https://github.com/akashbhaskar2011/vendor-management-system.git
    ```

2. Navigate to the project directory:

    ```bash
    cd vendor-management-system
    ```

3. Install dependencies using pipenv:

    ```bash
    pipenv install
    ```

4. Activate the virtual environment:

    ```bash
    pipenv shell
    ```

5. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

### API Endpoints

- **Vendor Profile Management:**
    - `POST /api/vendors/`: Create a new vendor.
    - `GET /api/vendors/`: List all vendors.
    - `GET /api/vendors/{vendor_id}/`: Retrieve a specific vendor's details.
    - `PUT /api/vendors/{vendor_id}/`: Update a vendor's details.
    - `DELETE /api/vendors/{vendor_id}/`: Delete a vendor.

- **Purchase Order Tracking:**
    - `POST /api/purchase_orders/`: Create a purchase order.
    - `GET /api/purchase_orders/`: List all purchase orders with an option to filter by vendor.
    - `GET /api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order.
    - `PUT /api/purchase_orders/{po_id}/`: Update a purchase order.
    - `DELETE /api/purchase_orders/{po_id}/`: Delete a purchase order.

- **Vendor Performance Evaluation:**
    - `GET /api/vendors/{vendor_id}/performance`: Retrieve a vendor's performance metrics.

### Additional Features

- **Generate Token Endpoint:**
    - `POST /api/generate_token/`: Generate an authentication token.

- **Purchase Orders by Vendor Endpoint:**
    - `GET /api/vendors/{vendor_id}/purchase_orders/`: Retrieve all purchase orders associated with a specific vendor.

## Models

### Vendor

- `name`: CharField - Vendor's name.
- `contact_details`: TextField - Contact information of the vendor.
- `address`: TextField - Physical address of the vendor.
- `vendor_code`: CharField - A unique identifier for the vendor.
- `on_time_delivery_rate`: FloatField - Tracks the percentage of on-time deliveries.
- `quality_rating_avg`: FloatField - Average rating of quality based on purchase orders.
- `average_response_time`: FloatField - Average time taken to acknowledge purchase orders.
- `fulfillment_rate`: FloatField - Percentage of purchase orders fulfilled successfully.

### PurchaseOrder

- `po_number`: CharField - Unique number identifying the PO.
- `vendor`: ForeignKey - Link to the Vendor model.
- `order_date`: DateTimeField - Date when the order was placed.
- `delivery_date`: DateTimeField - Expected or actual delivery date of the order.
- `items`: JSONField - Details of items ordered.
- `quantity`: IntegerField - Total quantity of items in the PO.
- `status`: CharField - Current status of the PO (e.g., pending, completed, canceled).
- `quality_rating`: FloatField - Rating given to the vendor for this PO (nullable).
- `issue_date`: DateTimeField - Timestamp when the PO was issued to the vendor.
- `acknowledgment_date`: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.

### HistoricalPerformance

- `vendor`: ForeignKey - Link to the Vendor model.
- `date`: DateTimeField - Date of the performance record.
- `on_time_delivery_rate`: FloatField - Historical record of the on-time delivery rate.
- `quality_rating_avg`: FloatField - Historical record of the quality rating average.
- `average_response_time`: FloatField - Historical record of the average response time.
- `fulfillment_rate`: FloatField - Historical record of the fulfillment rate.

