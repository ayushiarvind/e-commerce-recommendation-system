Step 1: Start the Flask Server
Open your terminal/command prompt.
Navigate to the folder where project.py (Flask server file) is located.
Run the following command to start the Flask server:
bash
Copy
Edit
python project.py
This will start the Flask server at http://127.0.0.1:5000/.

Step 2: Open the main.html Page
After starting the Flask server, open the main.html file in your browser.
On this page, you will see a "View Recommendations" button.
you will be directed to another page 

Step 3: Provide User ID and Recommendation Count
On the index.html page, you will be asked to enter:
User ID: Enter the user ID for whom you want to generate recommendations.
Top N Recommendations: Enter the number of recommendations you want (default is 5, but you can enter any number between 1 and 5).

Step 4: View Recommendations
After filling in the User ID and the number of recommendations, click on the "View Recommendations" button.



Step 5: See the Recommendations
On the recommendation.html page, the system will generate and display the top N recommended products for the given user ID.
The recommendations will include the item IDs and predicted ratings.

