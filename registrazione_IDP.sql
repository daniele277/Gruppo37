drop table if exists User;
drop table if exists Client;
drop table if exists AccessToken;
drop table if exists AuthorizationCode;

create table User (
	userID integer primary key autoincrement,
	name varchar(20),
	surname varchar(20),
	email varchar(20),
	hashPassword varchar(20),
	address varchar(20),
	city varchar(20),
	state varchar(20),
	zip integer
);

create table Client (
    clientID integer primary key autoincrement,
    name text,
    redirectURI text,
    grantType text,
    scope text,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    authEndpoint text,
    tokenEndpoint text
);


create table AccessToken (
    tokenID integer primary key autoincrement,
    tokenExpiryDate DATETIME,
    clientID integer,
    userID integer
);

create table AuthorizationCode (
    code text primary key,
    codeExpiryDate DATETIME,
    clientID integer,
    userID integer
);



