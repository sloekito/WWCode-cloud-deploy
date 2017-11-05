

CREATE TABLE IF NOT EXISTS `catalog`.`books` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL,
  `author` VARCHAR(255) NULL,
  `publisher` VARCHAR(255) NULL,
    PRIMARY KEY (`id`)
  );

INSERT IGNORE INTO `catalog`.`books`
    ( `title`, `author`, `publisher`)
VALUES
    ( "What Happened", "Hillary Clinton", "Simon & Schuster"),
    ( "The Glass Castle", "Jeannette Walls", "Scribner"),
    ( "Hillbilly Elegy", "J. D. Vance", "HarperCollins"),
    ( "Understanding Trump", "Newt Gingrich", "Center Street"),
    ( "Astrophysics for People in a Hurry", "Neil deGrasse Tyson", "Norton"),
    ( "Option B", "Sheryl Sandberg and Adam Grant", "Knopf"),
    ( "Old School: Life in the Sane Lane", "Bill O'Reilly and Bruce Feirstein", "Holt"),
    ( "Hidden Figures", "Margot Lee Shetterly", "Morrow/HarperCollins"),
    ( "Killing the Rising Sun", "Bill O'Reilly and Martin Dugard", "Holt"),
    ( "The Princess Diarist", "Carrie Fisher", "Blue Rider Press"),
    ( "The Zookeeper's Wife", "Diane Ackerman", "Norton"),
    ( "Shattered", "Jonathan Allen and Amie Parnes", "Crown"),
    ( "Rediscovering Americanism", "Mark Levin", "Simon & Schuster");


