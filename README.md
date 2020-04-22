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
 * [ ] Basic constructs like select, project, cartesian product, natural join
 * [ ] Aggregate functions like group by, sum, average, max etc
 * [ ] Nested subqueries
 * [X] Modification of the database like insert, update and delete
 
### 4 of the 6 items
 * [X] Views
    * Made in tools
    * Used in routes
    * Makes a view that looks like Items table but the addedByUid is replaced by User.username
 * [ ] Triggers (if no user agent  is given we can replace it with "[NONE GIVEN]")
 * [ ] Transaction processing (I think when we move items from one table to another counts)
 * [ ] Prepared Statements ()
 * [ ] Stored Procedures (maybe use functions that return some sql text)
 * [ ] Stored Functions


## Requirements
 * Python 3
  * flask_login
  * flask_sqlalchemy
  * flask_bcrypt
  * flask_wtf


