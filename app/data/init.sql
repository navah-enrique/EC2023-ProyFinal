create table venue_pre(
    Neighborhood varchar(80),
    Fst_Most_Common_Venue varchar(80),
    Snd_Most_Common_Venue varchar(80),
    Trd_Most_Common_Venue varchar(80),
    Foth_Most_Common_Venue varchar(80),
    Fith_Most_Common_Venue varchar(80),
    Sith_Most_Common_Venue varchar(80),
    Seth_Most_Common_Venue varchar(80),
    Eth_Most_Common_Venue varchar(80),
    Nth_Most_Common_Venue varchar(80),
    Tth_Most_Common_Venue varchar(80)   
);
COPY venue_pre
FROM '/data/venues_cdmx_paraentrenamiento.csv' 
DELIMITER ',' 
CSV HEADER
NULL as 'NA';
create table venue_completa(
    Neighborhood varchar(80),
    Neighborhood_Latitude float(24),
    Neighborhood_Longitude float(24),
    Venue varchar(100),
    Venue_Latitude float(24),
    Venue_Longitude float(24),
    Venue_Category varchar(80)  
);
COPY venue_completa
FROM '/data/venues_cdmx_completa.csv' 
DELIMITER ',' 
CSV HEADER
NULL as 'NA';
create table venue_kmeans(
    Neighborhood varchar(80),
    Neighborhood_Latitude float(24),
    Neighborhood_Longitude float(24),
    Venue varchar(100),
    Venue_Latitude float(24),
    Venue_Longitude float(24),
    Venue_Category varchar(80),
    Cluster_Label float(24), 
    Fst_Most_Common_Venue varchar(80),
    Snd_Most_Common_Venue varchar(80),
    Trd_Most_Common_Venue varchar(80),
    Foth_Most_Common_Venue varchar(80),
    Fith_Most_Common_Venue varchar(80),
    Sith_Most_Common_Venue varchar(80),
    Seth_Most_Common_Venue varchar(80),
    Eth_Most_Common_Venue varchar(80),
    Nth_Most_Common_Venue varchar(80),
    Tth_Most_Common_Venue varchar(80)   
);
COPY venue_pre
FROM '/data/venues_kmeans.csv' 
DELIMITER ',' 
CSV HEADER
NULL as 'NA';