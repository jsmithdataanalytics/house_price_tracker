-- migrate:up
CREATE TABLE `Listings` (
	`id` INTEGER PRIMARY KEY,
	`listing_id` TEXT NOT NULL UNIQUE,
	`listing_price` TEXT NOT NULL,
	`bedrooms` INTEGER,
	`outcode` TEXT,
	`listed_on` TEXT,
	`last_reduced_on` TEXT
);

-- migrate:down
DROP TABLE `Listings`;
