# Feature List for Invoice Tracker

## Brainstorm a list of features that you'd like the finished product to have. You are not expected to finish all, or even most, of the features you come up with. The goal is just to come up with some fun ideas that you can work towards. Add a docs folder to you repository and include this list as a markdown file.

This document outlines potential features for the Invoice Tracker project. These are ideas that we may or may not implement, but they serve as a roadmap for future development.

### Core Features
- *Google SSO Integration*: Implement Google Single Sign-On (SSO) to allow users to log in using their Google accounts.
- *Receipt Upload*: Enable logged-in users to upload receipts for processing and storage.
- *User Invitations*: Allow users to invite others to collaborate on receipt management.
- *Bill Splitting*: Implement a feature where users can split bills among invited participants.
- *Textual Insight*: Employ Gemini LLM to extract and analyze text from receipts, enhancing data accuracy and insights, and convert it to JSON.
- *Efficient Data Storage*: Store the extracted and processed data efficiently to optimize performance and retrieval.
- *Scanned History*: The List button feature allows users to view and track their previously uploaded receipts, displaying key details like vendor, date, amount, and location.
- *Modify*: Users can edit or delete their scanned receipts, allowing them to modify details or remove entries as needed for accurate record-keeping.
- *Data Storage*: The system stores data from uploaded receipts, making it easy to access and manage.

## Define the MVP (Minimum viable product) for your project. Out of your list of features select the most important subset. You will be expected to complete implementation of this list so try to keep the set of tasks manageable. Aim for something that you think can be completed in 2-4 weeks. Include the resulting list in your docs directory.


### Minimum Viable Product (MVP) - Invoice Tracker

This document outlines the Minimum Viable Product (MVP) for the Invoice Tracker project. The selected features represent the core functionalities that will be implemented within 2-4 weeks.

### MVP Feature List

1. *Receipt Upload*  
   - Enable users to upload receipts for processing and storage.

2. *Textual Insight*  
   - Utilize Gemini LLM to extract and analyze text from receipts.

3. *Data Storage*  
   - Efficiently store data extracted from uploaded receipts.  
   - Ensure easy access and management of stored records.

4. *Modify*  
   - Users can edit or delete their scanned receipts, allowing them to modify details or remove entries as needed for accurate record-keeping.



This MVP serves as the foundation for the Invoice Tracker project, ensuring essential functionalities are available before expanding to additional features.

## For each of the features that are to be included in the MVP, create one or more User stories. You'll estimate these tasks as part of your first sprint, so you don't need to be too precise yet, but try to keep them small. Any story that will take more than a week should be broken into multiple smaller stories if possible. Follow the user stories guidelines discussed in lecture. To track these user stories we'll be using GitHub Issues. Create an Issue for each user story in your project. All group member must create at least one user story.

1. *User Story: Receipt Upload*  
As a user,  
I want to be able to upload my receipts into the system,  
So that I can store my expenses in one place.

2. *User Story: Textual Insight*  
As a user,  
I want the system to extract text from my receipts automatically,  
So that I can easily view important information like amounts, dates, and vendors.

3. *User Story: Data Storage*  
As a user,  
I want the system to store the data extracted from my receipts,  
So that I can retrieve my expense records at any time.

4. *User Story: Modify*  
As a user,  
I want to be able to edit or delete my uploaded receipts,  
So that I can ensure the accuracy of my records and remove unnecessary entries.



## Discuss the overall structure your project will have. It's a good idea to break the project into several files in order to simplify the process of multiple people contributing to the project.


