Vendor Management System with Performance Metrics

This Vendor Management System is built using Django and Django REST Framework. It allows for the management of vendor profiles, tracking of purchase orders, and calculation of vendor performance metrics.

Setup Instructions
1. Clone the repository to your local machine:
   git clone <repository-url>
2. Navigate to the project directory:
   cd vendor-management-system
3. Create a virtual environment (optional but recommended):
   python -m venv venv
4. Activate the virtual environment:
   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
5. Install the required dependencies:
    pip install -r requirements.txt
6. Apply database migrations:
   python manage.py migrate
7. Run the development server:
   python manage.py runserver
   
The API should now be accessible at http://127.0.0.1:8000/.

Using the API Endpoints
Vendor Endpoints
1. GET /api/vendors/: List all vendors.
2. POST /api/vendors/: Create a new vendor.
3. GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
4. PUT /api/vendors/{vendor_id}/: Update a vendor's details.
5. DELETE /api/vendors/{vendor_id}/: Delete a vendor.
   
Purchase Order Endpoints
1. GET /api/purchase_orders/: List all purchase orders.
2. POST /api/purchase_orders/: Create a new purchase order.
3. GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
4. PUT /api/purchase_orders/{po_id}/: Update a purchase order.
5. DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
6. POST /api/purchase_orders/{po_id}/acknowledge/: Acknowledge a purchase order.
   
Vendor Performance Endpoint
1. GET /api/vendors/{vendor_id}/performance/: Retrieve performance metrics for a specific vendor.


Running the Test Suite
To run the test suite for the Vendor Management System, follow these steps:

1. Ensure that you have activated your virtual environment.
2. Navigate to the project directory.
3. Run the following command:
   python manage.py test

This will execute all the tests in the project and display the results in the terminal.
