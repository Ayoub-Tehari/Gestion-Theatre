create table LesZones (
    noZone integer,
    catZone varchar (50) not null,
    tauxZone decimal (4,2) not null,
    constraint pk_zon_noZone primary key (noZone),
    constraint ck_zon_noZone check (noZone > 0),
    constraint ck_zon_tauxZone check (tauxZone >= 0),
    constraint ck_zon_cat check (catZone in ('orchestre', 'balcon', 'poulailler'))
);

create table LesCategoriesTickets (
    libelleCat varchar(50) not null,
    tauxReductionCat decimal (4,2) ,
    constraint pk_catTck_libelleC primary key (libelleCat),
    constraint ck_catTck_tauxReductionCat check (tauxReductionCat >= 0 and tauxReductionCat <=1)
);

create table LesTickets (
    noSpec integer,
    dateRep date,
    noPlace integer,
    noRang integer,
    dateEmTick date,
    libelleCat varchar(50),
    noDos integer not null,
    constraint pk_tck_place_rep unique (noSpec, dateRep, noPlace, noRang),
    constraint fk_tck_numS_dateR foreign key (noSpec, dateRep) references LesRepresentations_base(noSpec, dateRep),
    constraint fk_tck_noP_noR foreign key (noPlace, noRang) references LesPlaces (noPlace,noRang),
    constraint fk_tck_noD foreign key (noDos) references LesDossiers_base (noDos),
    constraint fk_tck_libelleC foreign key (libelleCat) references LesCategoriesTickets (libelleCat),
    constraint ck_dates check (dateEmTick < dateRep)
);

create table LesSpectacles (
    noSpec integer,
    nomSpec varchar(50) not null,
    prixBaseSpec decimal (6,2) not null,
    constraint pk_spec_noSpec primary key (noSpec),
    constraint ck_spec_noSpec check (noSpec > 0),
    constraint ck_spec_prixBaseSpec check (prixBaseSpec >= 0)
);

create table LesRepresentations_base (
    noSpec integer,
    dateRep date,
    promoRep decimal (4,2) not null,
    constraint pk_rep_noSpec_dateRep primary key (noSpec, dateRep),
    constraint fk_rep_noSpec foreign key (noSpec) references LesSpectacles(noSpec),
    constraint ck_rep_promoRep check (promoRep >= 0 and promoRep <=1)
);

create table LesPlaces (
    noPlace integer,
    noRang integer,
    noZone integer not null,
    constraint pk_pl_noP_noR primary key (noPlace, noRang),
    constraint fk_pl_numZ foreign key (noZone) references LesZones(noZone),
    constraint ck_pl_noP check (noPlace > 0),
    constraint ck_pl_noR check (noRang > 0)
);

create table LesDossiers_base (
    noDos integer,
    constraint pk_dos_noD primary key (noDos)
);


create view LesRepresentations as
select noSpec, dateRep, promoRep, (select count(*)as n from "LesPlaces") - count(noPlace) as nbPlacesDispoRep
from LesRepresentations_base natural left join "LesTickets" group by noSpec, dateRep, promoRep;

create view LesDossiers as
    select noDos, sum("prixBaseSpec") * "promoRep" * "tauxZone" * "tauxReductionCat" as montant
from "LesTickets" natural join "LesSpectacles" natural join "LesRepresentations_base"
natural join "LesPlaces" natural join "LesZones" natural join "LesCategoriesTickets"
group by "noDos", "promoRep", "tauxZone", "tauxReductionCat"
;

-- TODO 1.2 : ajouter la définition de la vue LesRepresentations
-- TODO 1.3 : ajouter la table LesCategoriesTickets
-- TODO 1.4 : ajouter la définition de la vue LesDossiers
