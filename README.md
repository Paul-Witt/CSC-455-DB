# CSC-455-DB

## Rubric
### Functionality proposed
 * [X] User table (created in models, used in routes)
 * [X] Sessions ( created in models, used in routes when user logs in)
 * [X] Items (created in models, used in routes)
 * [X] RemovedItems (created in models, used in routes)

### Database-related elements
 * [X] Primary keys (satisfied in models)
 * [X] Foreign keys, including cascade specifications
    * Made in tools
    * when a user is deleted it removes all items they posted

### Queries
 * [X] Basic constructs like select, project, cartesian product, natural join
    * easy one since we cant do anything with out these
 * [X] Aggregate functions like group by, sum, average, max etc 
    * max used in the trigger
 * [X] Nested subqueries (the view made in tools.py>addViews satisfies this)
    * Used in the one of the views
 * [X] Modification of the database like insert, update and delete
 
### 4 of the 6 items
 * [X] Views
    * Made in tools
    * Used in routes
    * Makes a view that looks like Items table but the addedByUid is replaced by User.username
    * Makes a view that looks like removedItems table but the Uids are replaced by the usernames
    * Makes a view that looks like session table but the Uids are replaced by the usernames
 * [X] Triggers
    * Made in tools
    * Used when inserting into the items 
    * Adds one to the user who just posted an item
 * [X] Transaction processing (I think when we move items from one table to another counts)
 * [X] Prepared Statements (Used in routes when deleting a user)
 * [ ] Stored Procedures (Can't)
 * [ ] Stored Functions (Can't)

## Requirements
 * Python 3
  * flask_login
  * flask_sqlalchemy
  * flask_bcrypt
  * flask_wtf


