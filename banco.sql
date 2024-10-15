
CREATE DATABASE erp_sistema;
USE erp_sistema;

CREATE TABLE produtos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100),
  quantidade_estoque INT,
  preco_venda DECIMAL(10, 2)
);

CREATE TABLE clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100),
  telefone VARCHAR(20),
  email VARCHAR(100)
);

CREATE TABLE vendas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cliente_id INT,
  produto_id INT,
  quantidade INT,
  valor_total DECIMAL(10, 2),
  data_venda DATE,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id),
  FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

CREATE TABLE fornecedores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100),
  telefone VARCHAR(20),
  email VARCHAR(100)
);

CREATE TABLE compras (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fornecedor_id INT,
  produto_id INT,
  quantidade INT,
  valor_total DECIMAL(10, 2),
  data_compra DATE,
  FOREIGN KEY (fornecedor_id) REFERENCES fornecedores(id),
  FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

CREATE TABLE financeiro (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tipo ENUM('Entrada', 'Saída'),
  valor DECIMAL(10, 2),
  descricao VARCHAR(255),
  data DATE
);
