CREATE TABLE schema_migrations (version varchar(255) primary key);
CREATE TABLE `Listings` (
	`id` INTEGER PRIMARY KEY,
	`listing_id` TEXT NOT NULL UNIQUE,
	`listing_price` TEXT NOT NULL,
	`bedrooms` INTEGER,
	`outcode` TEXT,
	`listed_on` TEXT,
	`last_reduced_on` TEXT
);
-- Dbmate schema migrations
INSERT INTO schema_migrations (version) VALUES
  ('20200424005527');
