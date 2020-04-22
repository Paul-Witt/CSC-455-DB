# CSC-455-DB
## TODO
 * Foreigns keys might not be implemented right
 * Administrate Users page
 * Log sessions in table when user logs in
 * Implement views

## Rubric
### Functionality proposed
 * [X] User table (created in models, used in routes)
 * [X] Sessions (created in models, used in routes)
 * [X] Items (created in models, used in routes)
 * [X] RemovedItems (created in models, used in routes)

### Database-related elements
 * [X] Primary keys (satisfied in models)
 * [ ] Foreign keys, including cascade specifications

### Queries
 * [X] Basic constructs like select, project, cartesian product, natural join
      * easy one since we cant do anything with out these
 * [ ] Aggregate functions like group by, sum, average, max etc 
 * [ ] Nested subqueries
 * [X] Modification of the database like insert, update and delete
 
### 4 of the 6 items
 * [X] Views
    * Made in tools
    * Used in routes
    * Makes a view that looks like Items table but the addedByUid is replaced by User.username
    * Makes a view that looks like removedItems table but the Uids are replaced by the usernames
 * [ ] Triggers 
 * [ ] Transaction processing (I think when we move items from one table to another counts)
 * [ ] Prepared Statements ()
 * [ ] Stored Procedures (Can't)
 * [ ] Stored Functions (Can't)

## Requirements
 * Python 3
  * flask_login
  * flask_sqlalchemy
  * flask_bcrypt
  * flask_wtf


