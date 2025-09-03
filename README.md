# Projeto-C07---L2
# Consulado Digital – Sistema de Emissão de Vistos

 Visão Geral
O Consulado Digital é um sistema de banco de dados desenvolvido para gerenciar o processo de solicitação e emissão de vistos em um consulado.  
Ele organiza as informações de solicitantes, passaportes, vistos, entrevistas e funcionários consulares, garantindo rastreabilidade e segurança em cada etapa do processo.

Este projeto tem como objetivo modelar as entidades e os relacionamentos necessários para acompanhar o fluxo de emissão de vistos, desde a solicitação inicial até a aprovação ou recusa.

---

 Escopo do Projeto
O sistema cobre as seguintes operações:
- Cadastro de **solicitantes** e vinculação com seus **passaportes**.
- Registro das **solicitações de visto**, com histórico de status (pendente, aprovado, negado).
- Controle das **entrevistas agendadas**, associadas a vistos e conduzidas por funcionários.
- Gerenciamento de **funcionários do consulado** responsáveis pelas entrevistas e análises.

---

 Entidades e Atributos

 1. **Solicitante**
Representa a pessoa que solicita o visto.  
Atributos principais:
- ID_Solicitante (PK)
- Nome completo
- Data de nascimento
- Nacionalidade
- Endereço
- Contato (telefone/email)

 2. **Passaporte**
Documento oficial do solicitante.  
Atributos principais:
- ID_Passaporte (PK)
- Número do passaporte
- Data de emissão
- Data de validade
- País emissor
- ID_Solicitante (FK)

 3. **Visto**
Registro da solicitação de visto.  
Atributos principais:
- ID_Visto (PK)
- Tipo de visto (turismo, estudo, trabalho, etc.)
- Data de solicitação
- Status (pendente, aprovado, negado)
- ID_Solicitante (FK)

 4. **Entrevista**
Registro da entrevista do solicitante no consulado.  
Atributos principais:
- ID_Entrevista (PK)
- Data e hora
- Local (sala/guichê)
- Observações
- ID_Visto (FK)

 5. **Funcionário**
Representa os funcionários do consulado.  
Atributos principais:
- ID_Funcionario (PK)
- Nome completo
- Cargo
- Departamento
- Contato (telefone/email)

6. **Funcionario_Entrevista**

Tabela associativa que representa a participação de funcionários em entrevistas.
- ID_Funcionario (FK)
- ID_Entrevista (FK)
- (PK composta: ID_Funcionario + ID_Entrevista)

---

 Relacionamentos

- **Solicitante <-> Passaporte (1:1)**  
  Um solicitante possui um único passaporte válido, e cada passaporte pertence a apenas um solicitante.

- **Solicitante <-> Visto (1:N)**  
  Um solicitante pode realizar várias solicitações de visto ao longo do tempo, mas cada visto pertence a apenas um solicitante.

- **Visto <-> Entrevista (1:N)**  
  Um visto pode estar vinculado a várias entrevistas (ex.: reagendamentos), mas cada entrevista refere-se a apenas um visto.

- **Funcionário <-> Entrevista (N:M)**  
  Um funcionário pode conduzir várias entrevistas, e uma entrevista pode envolver mais de um funcionário (ex.: analista + tradutor).

---

## Resumo das Cardinalidades
- **1:1** → Solicitante – Passaporte  
- **1:N** → Solicitante – Visto  
- **1:N** → Visto – Entrevista  
- **N:M** → Funcionário – Entrevista  

---

## Autores
- Pedro Armengol de Oliveira - GEC - 2093  
- João Victor Batista Costa - GEC - 2107  

---
