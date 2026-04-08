use bibliogestor;

create table Libros (
	isbn int(13) not null primary key,
    titulo varchar(50) not null,
    autores varchar(80) not null,
    editorial varchar(50) not null,
    año year not null,
    categoría varchar(50),
    descripción varchar (250)
    );

create table ejemplaresFisicos(
	idEjemplar int(25) not null primary key,
    codigoIsbn int(13) not null, 
    constraint fk_codigoIsbn 
    foreign key (codigoIsbn) references Libros(isbn),
    ubicación varchar(10) not null,
    estado varchar(12) not null
    );

create table usuarios (
	codigo int(10) primary key,
    identificación int(10) not null,
    nombre varchar(30) not null,
    apellido varchar(30)not null,
    correo varchar(30) not null,
    rol bool not null,
    estado bool not null,
    carrera varchar(50)
    );

create table prestamos (
	idPrestamo int(25) primary key,
    codigoUsuario int(10) not null, 
    constraint fk_codigoUsuario 
    foreign key(codigoUsuario) references Usuarios(codigo),
    ejemplar varchar(50) not null,
    fechaPrestamo datetime not null,
    fechaVencimiento datetime not null
    );

 create table devoluciones(
	idDevolucion int(20) primary key,
    idPrestamo int(25) not null,
    constraint fk_idPrestamo foreign key(idPrestamo) references prestamos(idPrestamo),
    observaciones varchar(100)
    );
    



    
    