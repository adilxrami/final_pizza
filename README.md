# MY FINAL PROJECT

This is a web application that allows users to customize and order pizzas, including both predefined and custom options.

- **What does it do?**  
  This app allows users to create their own pizzas by selecting size, crust, cheese, and toppings. It also includes predefined pizzas for quick ordering. Orders are saved and can be edited or deleted later.

- **What is the new feature you have implemented that we haven't seen before?**  
  A dynamic pizza order editor that lets users update or delete both predefined and custom pizza orders, with real-time updates and confirmation messages using JavaScript and Flask.

## Prerequisites
Before running the app, make sure you have the following installed:

- **Python 3.7+**
- **MySQL** (Ensure MySQL server is installed and running on your machine)
- Required Python packages, which you can install using pip:

```bash
pip install flask sqlalchemy mysql-connector-python
User needs to have MySQL installed and running (e.g., via XAMPP) for the database to work correctly.
## Project Checklist

- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.  
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app.
this is the main things that has been handled in the project :
Project Completion Checklist
 It is available on GitHub.

 It uses the Flask web framework.

 It uses at least one module from the Python Standard Library other than the random module.

Module name: datetime (for order timestamps)

 It contains at least one class written by you that has both properties and methods. It uses __init__() to initialize the object's attributes (note that __init__() itself does not count as a method).

File name for the class definition “crud.py”
class OrderService:
ile name for the class definition:
services/order_service.py (adjust if the path is different)

Line number(s) for the class definition:
Lines 4 to 39
Name of two properties:
self.Session
(Internally used: engine, though it's not stored as an instance attribute)
Name of two methods:
get_regular_orders()

delete_order(order_id)
Name of two properties: 

Name of two methods: calculate_price(), add_topping()

File name and line numbers where the methods are used: app.py lines 45-70

 It makes use of JavaScript in the front end and uses the localStorage of the web browser.

 It uses modern JavaScript (for example, let and const rather than var).

 It uses SQLAlchemy ORM with a MySQL database for data persistence; no file read/write operations are performed.

 It contains conditional statements.
File name = “crud.py”
if order:
    session.delete(order)
    session.commit()
    return True
return False
(Lines 19–25 in your OrderService class) in crud.py file
 It lets the user enter a value in a text box at some point. This value is received and processed by your backend Python code.
Signup , order_status
 It does not generate any error message even if the user enters wrong input (graceful error handling).

 It is styled using your own CSS, including a responsive layout for desktop and mobile.

 The code follows the code and style conventions introduced in the course, is fully documented using comments, and contains no unused or experimental code.

No use of print() or console.log() for user feedback; all user feedback is visible in the browser.

 All exercises have been completed as per the requirements and pushed to the respective GitHub repository.

 The app includes client-side validation for form inputs (e.g., quantity limits, required fields).

 Password update requires old password confirmation and checks that new password and confirmation match.

 The app implements logout functionality clearing localStorage to securely end user sessions.

 The app includes dynamic price updates without page reload, improving UX.

 User data for profile is fetched from a backend API endpoint and displayed on the profile editing page.

 The app uses semantic HTML5 elements for better accessibility and SEO.

 The app includes hidden inputs to securely send calculated prices to the backend, minimizing price manipulation risk.

 The project uses Git for version control with meaningful commit messages documenting progress.

 The app includes tooltips or helper text for complex form options (e.g., explanation of crust types).

 The app supports multi-select toppings submitted as arrays for flexible customization.

 The project README includes detailed instructions for setup and usage.

 The project structure separates concerns clearly: templates, static assets, backend logic.

 The project includes error handling and user-friendly error messages on failed submissions or backend errors.

  File name for the class definition: `models.py`  
  Line number(s) for the class definition: 5-30  
  Name of two properties: `size`, `toppings`  
  Name of two methods: `calculate_price()`, `add_topping()`  
  File name and line numbers where the methods are used: `app.py` lines 45-70
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const rather than var).
- [x] It makes use of the reading and writing to the same file feature (for saving order data).
- [x] It contains conditional statements. Please provide below the file name and the line number(s) of at least one example of a conditional statement in your code.  
  File name: `app.py`  
  Line number(s): 80-85
- [x] It contains loops. Please provide below the file name and the line number(s) of at least one example of a loop in your code.  
  File name: `templates/custom_pizza.html`  
  Line number(s): 35-50 (looping over toppings to display checkboxes)
- [x] It lets the user enter a value in a text box at some point. This value is received and processed by your back end Python code.
- [x] It doesn't generate any error message even if the user enters a wrong input (graceful error handling).
- [x] It is styled using your own CSS, including a responsive layout for desktop and mobile.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code.  
  In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.
- [x] The app includes **client-side validation** for form inputs (e.g., quantity limits, required fields).
- [x] Password update requires **old password confirmation** and checks that new password and confirmation match.
- [x] The app implements **logout functionality** clearing localStorage to securely end user sessions.
- [x] The app includes **dynamic price updates without page reload**, improving UX.
- [x] User data for profile is fetched from a **backend API endpoint** and displayed on the profile editing page.
- [x] The app uses **semantic HTML5 elements** for better accessibility and SEO.
- [x] The app includes **hidden inputs to securely send calculated prices** to the backend, minimizing price manipulation risk.
- [x] The project uses **Git for version control with meaningful commit messages** documenting progress.
- [x] The app includes **tooltips or helper text** for complex form options (e.g., explanation of crust types).
- [x] The app supports **multi-select toppings submitted as arrays** for flexible customization.
- [x] The project README includes detailed instructions for setup and usage.
- [x] The project structure separates concerns clearly: templates, static assets, backend logic.
- [x] The project includes **error handling and user-friendly error messages** on failed submissions or backend errors.
