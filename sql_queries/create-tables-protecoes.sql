CREATE TABLE Despacho (
  despachoId INT AUTO_INCREMENT PRIMARY KEY,
  codigoDespacho VARCHAR(255) NOT NULL,
  descricaoDespacho VARCHAR(255) NOT NULL,
  comentario VARCHAR(255),
  prazoCumprimento INT NOT NULL,
  afetaExigencia BOOLEAN NOT NULL
) COMMENT '';

CREATE TABLE RevistaPropriedadeIndustrial (
  rpiId INT AUTO_INCREMENT PRIMARY KEY,
  numeroRpi VARCHAR(255) NOT NULL,
  dataPublicacao DATE NOT NULL,
  diretoria VARCHAR(255) NOT NULL
) COMMENT '';

CREATE TABLE Exigencia (
  exigenciaId INT AUTO_INCREMENT PRIMARY KEY,
  despachoId INT,
  rpiId INT,
  protecaoId INT,
  FOREIGN KEY (despachoId) REFERENCES Despacho(despachoId),
  FOREIGN KEY (rpiId) REFERENCES RevistaPropriedadeIndustrial(rpiId)
) COMMENT '';

