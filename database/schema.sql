-- MySQL Schema for BiblioGestor
-- Character set: utf8mb4 (supporting Spanish characters like ñ, í, ó, etc.)

CREATE DATABASE IF NOT EXISTS `bibliogestor` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `bibliogestor`;

-- 1. Tabla: usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
    `codigo` VARCHAR(20) NOT NULL,
    `identificación` VARCHAR(20) NOT NULL,
    `nombre` VARCHAR(100) NOT NULL,
    `apellido` VARCHAR(100) NOT NULL,
    `correo` VARCHAR(150) NOT NULL,
    `rol` TINYINT(1) NOT NULL COMMENT '1 = Estudiante, 0 = Otro/Personal',
    `estado` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '1 = Activo, 0 = Inactivo',
    `carrera` VARCHAR(100) DEFAULT NULL,
    PRIMARY KEY (`codigo`),
    UNIQUE KEY `uq_usuarios_identificacion` (`identificación`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Tabla: libros
CREATE TABLE IF NOT EXISTS `libros` (
    `isbn` VARCHAR(20) NOT NULL,
    `titulo` VARCHAR(255) NOT NULL,
    `autores` VARCHAR(255) NOT NULL,
    `editorial` VARCHAR(255) DEFAULT NULL,
    `año` INT DEFAULT NULL,
    `categoría` VARCHAR(100) DEFAULT NULL,
    `descripción` TEXT DEFAULT NULL,
    PRIMARY KEY (`isbn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Tabla: ejemplaresfisicos
CREATE TABLE IF NOT EXISTS `ejemplaresfisicos` (
    `idEjemplar` VARCHAR(50) NOT NULL,
    `codigoIsbn` VARCHAR(20) NOT NULL,
    `ubicación` VARCHAR(255) DEFAULT NULL,
    `estado` VARCHAR(50) NOT NULL DEFAULT 'Disponible' COMMENT 'Disponible, Prestado, Perdido, etc.',
    PRIMARY KEY (`idEjemplar`),
    CONSTRAINT `fk_ejemplares_libros` FOREIGN KEY (`codigoIsbn`) REFERENCES `libros` (`isbn`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Tabla: prestamos
CREATE TABLE IF NOT EXISTS `prestamos` (
    `idPrestamo` INT NOT NULL,
    `codigoUsuario` VARCHAR(20) NOT NULL,
    `ejemplar` VARCHAR(50) NOT NULL,
    `fechaPrestamo` DATETIME NOT NULL,
    `fechaVencimiento` DATETIME NOT NULL,
    `estadoPrestamo` VARCHAR(50) NOT NULL DEFAULT 'En solicitud' COMMENT 'En solicitud, Aprobada, Rechazada',
    PRIMARY KEY (`idPrestamo`),
    CONSTRAINT `fk_prestamos_usuarios` FOREIGN KEY (`codigoUsuario`) REFERENCES `usuarios` (`codigo`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_prestamos_ejemplares` FOREIGN KEY (`ejemplar`) REFERENCES `ejemplaresfisicos` (`idEjemplar`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Tabla: devoluciones
CREATE TABLE IF NOT EXISTS `devoluciones` (
    `idDevolucion` INT NOT NULL,
    `idPrestamo` INT NOT NULL,
    `observaciones` TEXT DEFAULT NULL,
    `estadoDevolucion` VARCHAR(50) NOT NULL DEFAULT 'En solicitud' COMMENT 'En solicitud, Aprobada, Rechazada',
    `fechaDevolucion` DATETIME NOT NULL,
    `tarifaCobro` DECIMAL(10,2) DEFAULT 0.00,
    PRIMARY KEY (`idDevolucion`),
    CONSTRAINT `fk_devoluciones_prestamos` FOREIGN KEY (`idPrestamo`) REFERENCES `prestamos` (`idPrestamo`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Tabla: reservas
CREATE TABLE IF NOT EXISTS `reservas` (
    `idReserva` INT NOT NULL AUTO_INCREMENT,
    `codigoUsuario` VARCHAR(20) NOT NULL,
    `idEjemplar` VARCHAR(50) NOT NULL,
    `fechaReserva` DATETIME NOT NULL,
    `estadoReserva` VARCHAR(50) NOT NULL DEFAULT 'Activa' COMMENT 'Activa, Completada, Cancelada',
    PRIMARY KEY (`idReserva`),
    CONSTRAINT `fk_reservas_usuarios` FOREIGN KEY (`codigoUsuario`) REFERENCES `usuarios` (`codigo`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_reservas_ejemplares` FOREIGN KEY (`idEjemplar`) REFERENCES `ejemplaresfisicos` (`idEjemplar`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
