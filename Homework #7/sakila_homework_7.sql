-- use database --
USE sakila;

-- 1a. display first and last name --
SELECT first_name, last_name FROM actor;

-- 1b. merge first and last name --
SELECT CONCAT(first_name,' ', last_name) AS Actor_Name FROM actor;

-- 2a. find actor id for Joe --
SELECT actor_id, first_name, last_name FROM actor
WHERE first_name = "JOE";

-- 2b. all actors with last names containing the letter GEN --
SELECT * FROM actor 
WHERE last_name LIKE "%GEN%";

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order --
SELECT last_name, first_name FROM actor 
WHERE last_name LIKE "%LI%"
ORDER BY last_name DESC;

-- 2d. display specific countries using IN --
SELECT country_id, country FROM country
WHERE country IN ("Afghanistan", "Bangladesh", "China");

-- 3a. add description col using BLOB --
ALTER TABLE actor
ADD description BLOB;

-- 3b. drop description col --
ALTER TABLE actor
DROP COLUMN description;

-- 4a. List the last names of actors, as well as how many actors have that last name --
SELECT last_name, COUNT(last_name) AS counted_last_name FROM actor
GROUP BY last_name;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors --
SELECT last_name, COUNT(last_name) AS counted_last_name FROM actor
GROUP BY last_name
HAVING COUNT(last_name) > 1;

-- turn off safe mode to allow udpates --
SET SQL_SAFE_UPDATES = 0;
-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record --
UPDATE actor
SET first_name = "HARPO" 
WHERE first_name = "GROUCHO" AND last_name = "WILLIAMS";

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO. --
UPDATE actor
SET first_name = "GROUCHO" 
WHERE first_name = "HARPO" AND last_name = "WILLIAMS";

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it? --
SHOW CREATE TABLE address;
-- is this it? or do you want us to actually recreate the table --

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address --
SELECT s.first_name, s.last_name staff, a.address
FROM staff AS s
JOIN address AS a
USING (address_id);

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment. --
SELECT s.first_name, s.last_name, SUM(p.amount) AS "Total $ Aug 2005"
FROM payment AS p
JOIN staff AS s
USING (staff_id)
WHERE p.payment_date LIKE "%2005-08%"
GROUP BY s.staff_id;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join. --
SELECT f.title, COUNT(fa.actor_id) AS "# of Actors"
FROM film AS f
JOIN film_actor AS fa
USING (film_id)
GROUP BY f.title;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system? --
SELECT f.title, COUNT(i.film_id)
FROM inventory AS i
JOIN film AS f
USING (film_id)
WHERE f.title = "Hunchback Impossible";

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name: --
SELECT c.first_name, c.last_name, sum(p.amount) AS "Total Spend"
FROM customer AS c
JOIN payment AS p
USING (customer_id)
GROUP BY customer_id
ORDER BY last_name;

-- 7a. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English. --
SELECT title FROM film
WHERE (title LIKE "K%" OR title LIKE "Q%") IN
(SELECT language_id FROM language
WHERE name = "English");

-- 7b. Use subqueries to display all actors who appear in the film Alone Trip. --
SELECT first_name, last_name 
FROM actor
WHERE actor_id IN
	(SELECT actor_id 
	FROM film_actor
	WHERE film_id IN
		(SELECT film_id FROM film
		WHERE title = "Alone Trip"));
        
-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.
SELECT c.first_name, c.last_name, c.email, co.country
FROM customer AS c
JOIN address AS a
USING (address_id)
JOIN city AS cy
USING (city_id)
JOIN country AS co
USING (country_id)
WHERE country = "Canada";

-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as family films.
SELECT f.title, c.name AS "film category"
FROM film AS f
JOIN film_category AS fc
USING (film_id)
JOIN category AS c
USING (category_id)
WHERE name = "Family";

-- 7e. Display the most frequently rented movies in descending order.
SELECT f.title, COUNT(r.rental_date) AS "# of time rented"
FROM film AS f
JOIN inventory AS i
USING (film_id)
JOIN rental AS r
USING (inventory_id)
GROUP BY f.title
ORDER BY COUNT(r.rental_date) DESC;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
SELECT sum(p.amount) AS "Total Sales $", s.store_id
FROM payment AS p
JOIN staff
USING (staff_id)
JOIN store AS s
USING (store_id)
GROUP BY s.store_id;

-- 7g. Write a query to display for each store its store ID, city, and country.
SELECT s.store_id, c.city, co.country
FROM store AS s
JOIN address AS a
USING (address_id)
JOIN city AS c
USING (city_id)
JOIN country AS co
USING (country_id);

-- 7h. List the top five genres in gross revenue in descending order.
SELECT * from category;

SELECT c.name AS "genres", SUM(p.amount) AS "gross revenue"
FROM payment AS p
JOIN rental
USING (rental_id)
JOIN inventory
USING (inventory_id)
JOIN film_category
USING (film_id)
JOIN category AS c
USING (category_id)
GROUP BY c.name
ORDER BY SUM(p.amount) DESC LIMIT 5;

-- 8a create a view of 7h
CREATE VIEW top_five_grossing_generes AS
SELECT c.name AS "genres", SUM(p.amount) AS "gross revenue"
FROM payment AS p
JOIN rental
USING (rental_id)
JOIN inventory
USING (inventory_id)
JOIN film_category
USING (film_id)
JOIN category AS c
USING (category_id)
GROUP BY c.name
ORDER BY SUM(p.amount) DESC LIMIT 5;

-- 8b display view from 8a
SELECT * FROM top_five_grossing_generes;

-- 8c delete view (8a)
DROP VIEW top_five_grossing_generes;

