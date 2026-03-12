--  SQL  --

-- Mode 1 (Default): Run in container
-- Don't move any command and run docker-compose as the tutorial in README.md

-- Mode 2: Run out of container
-- (1) Install PostgreSQL
-- (2) Release the following notes begin with '---'
-- (3) run in bash / pwsh: $ psql -f setup.postgres.sql
--- create database WebsitePortfolio;
--- \c WebsitePortfolio

--  Tables  --
create table Person (
	id varchar(15) not null primary key,
	name varchar(20) null,
	pw varchar(24) not null,
	headp decimal(15, 0) null,
	email varchar(30) not null unique,
	leaved boolean not null default 'false'
);

create table PersonInfo (
	id varchar(15) not null primary key foreign key references Person(id),
	address varchar(30) null,
	gender decimal(1, 0) null,
	birth decimal(9, 0) null,
	desciption varchar(50) null,
	bguri decimal(15, 0) null,
	outlink varchar(20) null,
	signdate date not null default current_date
);

create table PersonIp (
	id varchar(15) not null foreign key references Person(id),
	ip inet not null,
	logdate date not null default current_date,
	logout boolean not null default 'false',
	primary key(id, ip)
);

create type itemtype as enum('proj', 'mntd', 'news');

create table Item (
	itype itemtype not null,
	id decimal(4, 0) not null,
	primary key(itype, id),
	title varchar(30) null,
	removed boolean not null default 'false'
);

create index idx_item_typeid on Item (itype);

create table Auth (
	person varchar(15) not null foreign key references Person(id),
	itype itemtype not null,
	itemid decimal(4, 0) not null,
	role decimal(1, 0) not null,
	primary key(person, itype, itemid),
	foreign key(itype, itemid) references Item(itype, id)
);

create table LinguoType (
	id char(2) not null primary key
);
copy LinguoType (id) from stdin;
en
fr
de
es
it
no
zh
jp
ko
pt
\.

create table Linguo (
	id char(2) not null primary key,
	type char(2) not null foreign key references LinguoType(id),
	description varchar(20) not null,
	description_en varchar(20) null
);
copy Linguo (id, type, description, description_en) from stdin;
us	en	English (United States)	English (United States)
uk	en	English (United Kingdom)	English (United Kingdom)
fr	fr	Français	French
de	de	Deutsch	German
es	es	español	Spanish
it	it	italiano	Italian
no	no	Norsk	Norwegian
cn	zh	中文 (简体)	Simplized Chinese
tw	zh	中文 (正體)	Traditional Chinese
hk	zh	中文 (香港)	Hong Kong Chinese
mo	zh	中文 (澳門)	Macau Chinese
jp	jp	日本語	Japanese
ko	ko	한국어	Korean
pt	pt	Português	Portuguese
\.

create table ItemContent (
	itype itemtype not null,
	id decimal(4, 0) not null,
	linguo char(2) not null foreign key references Linguo(id),
	content json not null,
	primary key(itype, id, linguo),
	foreign key(itype, id) references(Item(itype, id))
);

--  Procedures and Functions  --
create function getItems (
	itype itemtype default null,
	count int default 8
)
returns table (
	TypeID itemtype,
	ItemId decimal(4, 0),
	ItemTitle varchar(30),
	Author varchar(20),
	AuthorHead decimal(15, 0)
)
language sql
as $body$
begin
	select t.*, Person.name as Author, Person.headp as AuthorHead
		from (
			select Item.itype as TypeID, Item.id as ItemId, Item.title as ItemTitle
				row_number() over (partition by Item.itype order by Item.id desc) as rn
				from Item
				where removed = 'false' and (getItems.itype is null or Item.itype = getItems.itype)
		) t
		left outer join Auth
			on t.TypeID = Auth.itype and t.ItemId = Auth.itemid and Auth.role = 0
		left outer join Person
			on Auth.person = Person.id
		where rn <= count;
end;
$body$;

create procedure loginIp (
	person varchar(15),
	logip inet
)
language plpgsql
as $body$
begin
	insert into PersonIp (id, ip)
		values (person, logip)
	on conflict (id, ip) do update
		set logdate = current_date, logout = 'false';
end;
$body$;

create function checkLogin (
	person varchar(15),
	logip inet default null,
	pwd varchar(24) default null
)
returns table (
	checking boolean
)
language plpgsql
as $body$
begin
	if pwd is not null then
		select true as checking
			from Person
			where id = person and pw = crypt(pwd, pw) and leaved = 'false'
			limit 1;
		call loginIp(person, logip);
	elsif logip is not null then
		select true as checking
			from PersonIp
			where id = person
				and logout = 'false'
				and logdate >= current_date - interval '30 days'
				and logip in (
					select ip
						from PersonIp
						where id = person
						order by logdate desc
						limit 4
				)
			limit 1;
		if found then
			call loginIp(person, logip);
		end if;
	else
		select false as checking;
	end if;
end;
$body$;

create function getPersonInfo (
	id varchar(15),
	isBasic boolean default true,
)
returns table (
	name varchar(20),
	headp decimal(15, 0),
	email varchar(30),
	address varchar(30),
	gender decimal(1, 0),
	birth decimal(9, 0),
	description varchar(50),
	bguri decimal(15, 0),
	outlink varchar(20)
)
language sql
as $body$
begin
	select name, headp, email, address, gender, birth, desc, bguri, outlink
		from Person left outer join PersonInfo
			on Person.id = PersonInfo.id
		where Person.id = getPersonInfo.id and Person.leaved = 'false';
end;
$body$;

create procedure signPerson (
	id varchar(15),
	pw varchar(24),
	email varchar(30)
)
language plpgsql
as $body$
begin
	insert into PersonInfo (id, pw, email)
		values (signPerson.id, signPerson.pw, signPerson.email);
end;
$body$;

create procedure pushItem (
	ittype itemtype,
	itemid decimal(4, 0)
)
language sql
as $body$
begin
	insert into Item (itype, id)
		values (ittype, itemid);
end;
$body$;

create procedure removeItem (
	ittype itemtype,
	itemid decimal(4, 0)
)
language sql
as $body$
begin
	update Item
		set removed = 'true'
		where itype = ittype and id = itemid;
end;
$body$;

create trigger trg_Item_remove
after delete on Item
for each row
rollback complete;

create trigger trg_Person_remove
after delete on Person
for each row
rollback complete;

-- one owner
create function fun_Auth_role_0()
returns trigger
language plpgsql
as $body$
declare count_role int;
begin
	if new.role <> 0 then
		return new;
	end if;
	select count(*)
		into count_role
		from Auth
		where itype = new.itype and itemid = new.itemid and (id <> new.id or lower(tg_op) = 'insert') and role = 0;
	if count_role >= 1 then
		raise exception '', new.itype, new.itemid;
	end if;
	return new;
end;
$body$;

create trigger trg_Auth_role_0
before insert or update on Auth
for each row
execute function fun_Auth_role_0();

-- race condition
create unique index idx_uq_Auth_role
on Auth (itype, itemid)
where role = 0;