
-- ------------------------------------------------------- --
--                    CUD - MARÍN                          --
--                      MGSTICS                            --
--                     2017/2018                           --
--              TRABAJO DE FIN DE MÁSTER                   --
--  DISEÑO E IMPLEMENTACIÓN DE UNA PLATAFORMA WEB PARA     --
-- LA GESTIÓN DE INCIDENTES DE SEGURIDAD DE LA INFORMACIÓN --
--               ALUMNO: BLAS CHICA MARTOS.                --
-- ------------------------------------------------------- --
-- ------------------------------------------------------- --
--   BORRADO DE CLAVES FORÁNEAS, TABLAS, USUARIO Y BBDD.   --
-- ------------------------------------------------------- --


-- Se indica que se utilice la BD correspondiente:
USE soteria;


-- Claves foráneas
ALTER TABLE INCIDENTS
    DROP FOREIGN KEY STAFF_INCIDENTS;
	
ALTER TABLE INCIDENTS
    DROP FOREIGN KEY ENS_INCIDENTS;

-- ALTER TABLE INCIDENTS
--     DROP FOREIGN KEY CSIRT_INCIDENTS;

-- ALTER TABLE CSIRT
--     DROP FOREIGN KEY INCIDENTS_CSIRT;


-- Tablas
DROP TABLE CSIRT;

DROP TABLE ENS;

DROP TABLE INCIDENTS;

DROP TABLE STAFF;

DROP TABLE NOTIFIED;

-- Usuario:
DROP USER if exists 'soteria'@'localhost';

-- BBDD
DROP DATABASE if exists soteria;

-- End of file.

