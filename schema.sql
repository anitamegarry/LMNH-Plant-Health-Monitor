
USE plants;
GO

SET DATEFORMAT dmy;

IF OBJECT_ID('beta.recording', 'U') IS NOT NULL DROP TABLE beta.recording;
IF OBJECT_ID('beta.plant', 'U') IS NOT NULL DROP TABLE beta.plant;
IF OBJECT_ID('beta.country', 'U') IS NOT NULL DROP TABLE beta.country;
IF OBJECT_ID('beta.species', 'U') IS NOT NULL DROP TABLE beta.species;
IF OBJECT_ID('beta.botanist', 'U') IS NOT NULL DROP TABLE beta.botanist;


CREATE TABLE beta.country (
    country_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    country_code VARCHAR(2) NOT NULL UNIQUE,
    country_name VARCHAR(50) NOT NULL
);

CREATE TABLE beta.species (
    species_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    plant_name VARCHAR(30) UNIQUE
);

CREATE TABLE beta.botanist (
    botanist_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    botanist_first_name VARCHAR(20) NOT NULL,
    botanist_last_name VARCHAR(20) NOT NULL,
    botanist_email VARCHAR(30) NOT NULL UNIQUE,
    botanist_phone_number VARCHAR(20)
);

CREATE TABLE beta.plant (
    plant_id SMALLINT PRIMARY KEY,
    botanist_id SMALLINT NOT NULL,
    species_id SMALLINT NOT NULL,
    country_id SMALLINT NOT NULL,
    CONSTRAINT FK_plant_botanist FOREIGN KEY (botanist_id) REFERENCES beta.botanist(botanist_id),
    CONSTRAINT FK_plant_species FOREIGN KEY (species_id) REFERENCES beta.species(species_id),
    CONSTRAINT FK_plant_country FOREIGN KEY (country_id) REFERENCES beta.country(country_id)
);

CREATE TABLE beta.recording (
    recording_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    plant_id SMALLINT NOT NULL,
    recording_taken DATETIME NOT NULL,
    last_watered DATETIME,
    soil_moisture FLOAT,
    temperature FLOAT,
    CONSTRAINT FK_recording_plant FOREIGN KEY (plant_id) REFERENCES beta.plant(plant_id)
);


INSERT INTO beta.species 
    (plant_name)
VALUES
    ('epipremnum aureum'),
    ('venus flytrap'),
    ('corpse flower'),
    ('rafflesia arnoldii'),
    ('black bat flower'),
    ('pitcher plant'),
    ('wollemi pine'),
    ('bird of paradise'),
    ('cactus'),
    ('dragon tree'),
    ('asclepias curassavica'),
    ('brugmansia x candida'),
    ('canna striata'),
    ('colocasia esculenta'),
    ('euphorbia cotinifolia'),
    ('ipomoea batatas'),
    ('cuphea david verity'),
    ('manihot esculenta variegata'),
    ('musa basjoo'),
    ('salvia splendens'),
    ('anthurium'),
    ('cordyline fruticosa'),
    ('ficus'),
    ('palm trees'),
    ('dieffenbachia seguine'),
    ('spathiphyllum'),
    ('croton'),
    ('ficus elastica'),
    ('aloe vera'),
    ('sansevieria trifasciata'),
    ('philodendron hederaceum'),
    ('schefflera arboricola'),
    ('aglaonema commutatum'),
    ('monstera deliciosa'),
    ('tacca integrifolia'),
    ('psychopsis papilio'),
    ('saintpaulia ionantha'),
    ('gaillardia'),
    ('amaryllis'),
    ('caladium bicolor'),
    ('chlorophytum comosum'),
    ('araucaria heterophylla'),
    ('begonia'),
    ('medinilla magnifica'),
    ('calliandra haematocephala'),
    ('zamioculcas zamiifolia'),
    ('crassula ovata');

INSERT INTO beta.botanist
    (botanist_first_name, botanist_last_name, botanist_email, botanist_phone_number)
VALUES
    ('Carl', 'Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'),
    ('Gertrude', 'Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'),
    ('Eliza', 'Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948');

INSERT INTO beta.country
    (country_code, country_name) 
VALUES
    ('AF', 'Afghanistan'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AG', 'Antigua and Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia'),
    ('BA', 'Bosnia and Herzegovina'),
    ('BW', 'Botswana'),
    ('BR', 'Brazil'),
    ('BN', 'Brunei'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('CV', 'Cabo Verde'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo'),
    ('CD', 'Congo, Democratic Republic of the'),
    ('CR', 'Costa Rica'),
    ('CI', 'Côte d''Ivoire'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czechia'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('SZ', 'Eswatini'),
    ('ET', 'Ethiopia'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GR', 'Greece'),
    ('GD', 'Grenada'),
    ('GT', 'Guatemala'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('HN', 'Honduras'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KP', 'Korea (North)'),
    ('KR', 'Korea (South)'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', 'Lao People''s Democratic Republic'),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia'),
    ('MD', 'Moldova'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('ME', 'Montenegro'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('MK', 'North Macedonia'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('QA', 'Qatar'),
    ('RO', 'Romania'),
    ('RU', 'Russia'),
    ('RW', 'Rwanda'),
    ('KN', 'Saint Kitts and Nevis'),
    ('LC', 'Saint Lucia'),
    ('VC', 'Saint Vincent and the Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome and Principe'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('RS', 'Serbia'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('SS', 'South Sudan'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syria'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania'),
    ('TH', 'Thailand'),
    ('TL', 'Timor-Leste'),
    ('TG', 'Togo'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad and Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('GB', 'United Kingdom'),
    ('US', 'United States'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VE', 'Venezuela'),
    ('VN', 'Vietnam'),
    ('YE', 'Yemen'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe');

INSERT INTO beta.plant
    (plant_id, botanist_id, species_id, country_id)
VALUES
    (0, 1, 1, 24),
    (1, 2, 2, 185),
    (2, 1, 3, 128),
    (3, 3, 4, 24),
    (4, 1, 5, 53),
    (5, 1, 6, 77),
    (6, 3, 7, 32),
    (8, 3, 8, 42),
    (9, 2, 9, 65),
    (10, 2, 10, 43),
    (11, 2, 11, 185),
    (12, 3, 12, 185),
    (13, 3, 13, 65),
    (14, 2, 14, 185),
    (15, 2, 15, 177),
    (16, 2, 16, 185),
    (17, 1, 17, 78),
    (18, 1, 18, 65),
    (19, 2, 19, 23),
    (20, 1, 20, 163),
    (21, 3, 21, 24),
    (22, 2, 8, 65),
    (23, 3, 22, 65),
    (24, 1, 23, 85),
    (25, 2, 24, 165),
    (26, 1, 25, 3),
    (27, 1, 26, 182),
    (28, 1, 27, 185),
    (29, 2, 28, 85),
    (30, 1, 29, 99),
    (31, 2, 30, 36),
    (32, 2, 31, 65),
    (33, 1, 32, 77),
    (34, 2, 33, 163),
    (35, 1, 34, 35),
    (36, 2, 35, 185),
    (37, 3, 36, 77),
    (38, 2, 37, 171),
    (39, 1, 38, 85),
    (40, 3, 39, 61),
    (41, 1, 40, 77),
    (42, 1, 41, 26),
    (44, 2, 42, 112),
    (45, 2, 43, 185),
    (46, 3, 44, 104),
    (47, 3, 45, 83),
    (48, 1, 46, 138),
    (49, 3, 47, 112),
    (50, 1, 1, 24);


