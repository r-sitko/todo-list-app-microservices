# Todo list microservices architecture application

## Table of contents

- [Todo list microservices architecture application](#Todo-list-microservices-architecture-application)
  - [Table of contents](#Table-of-contents)
  - [Description](#Description)
  - [Project structure](#Project-structure)
  - [Cloning repository](#Cloning-repository)
  - [Prerequisites](#Prerequisites)
  - [Generating interfaces](#Generating-interfaces)
  - [Generating diagrams](#Generating-diagrams)
  - [Running tests](#Running-tests)
    - [Running integration tests](#Running-integration-tests)
    - [Running end2end tests](#Running-end2end-tests)
  - [Technology stack](#Technology-stack)
    - [User service technology stack](#User-service-technology-stack)
    - [Todo service technology stack](#Todo-service-technology-stack)
    - [Gateway API service technology stack](#Gateway-API-service-technology-stack)
    - [End2end tests technology stack](#End2end-tests-technology-stack)
  - [Diagrams](#Diagrams)
    - [Deployment diagram](#Deployment-diagram)
    - [Login user sequence diagram](#Login-user-sequence-diagram)
    - [Register user sequence diagram](#Register-user-sequence-diagram)
    - [Create todo sequence diagram](#Create-todo-sequence-diagram)
    - [Get todo sequence diagram](#Get-todo-sequence-diagram)
    - [Delete todo sequence diagram](#Delete-todo-sequence-diagram)
    - [Update todo sequence diagram](#Update-todo-sequence-diagram)
    - [List todo sequence diagram](#List-todo-sequence-diagram)

## Description

This project demonstrates microservices architecture based application.

Main application features:

- gRPC APIs
- SSL encryption between client and backend
- users can login and register accounts
- JWT token authorization
- gateway API
- logged users can create, get, list, update and delete todo list entries
- services use MySQL databases
- services are running in Docker containers

Application consists of three services:

- Gateway API service - SSL encryption, JWT token verification, authorization and orchestration
- User service - registering users, managing user accounts, authentication and JWT token generation
- Todo service - creating, updating, deleting and querying todos

## Project structure

```
.
├── gateway - directory with gateway service
│   ├── inc
│   │   └── gateway - directory with header files
│   ├── src - directory with source code files
│   └── third_party - external dependencies (libraries)
│       └── jwt-cpp
├── protos - directory with gRPC interfaces
│   ├── todo - directory with gRPC interface for todo service
│   └── user - directory with gRPC interface for user service
├── test - directory with end2end tests
│   └── certs - directory with test certificates
├── todo - directory with source code and tests for todo service
│   ├── tests
│   │   └── integration - directory with integration tests for todo service
│   │       └── certs - directory with test certificates
│   └── todo - package with todo service code
└── user - directory with source code and tests for user service
    ├── tests
    │   └── integration - directory with integration tests for user service
    │       └── certs - directory with test certificates
    └── user - package with user service code
```

## Cloning repository

```bash
git clone --recursive https://github.com/rsitko92/todo-app-microservices.git
```

## Prerequisites

- [Docker](https://www.docker.com)
- [Docker Compose](https://www.docker.com)
- [PlantUML](http://plantuml.com) (if you want to generate diagrams)

## Generating interfaces

Being in root directory of project run:

```bash
sudo protos/run.sh
```

Generated interfaces definitions will be placed in `protos/.gen` directory. It is sufficient to generate they only one time.

## Generating diagrams

Being in root directory of project run:

```bash
docs/diagrams/generate.sh
```

Generated images with diagrams will be placed in `docs/diagrams/out` directory.

## Running tests

Before running any kind of tests (integration or end2end) generate the gRPC client and server interfaces from .proto service definitions files. See section [Generating interfaces](#generating-interfaces).

### Running integration tests

- User service:

  Being in root directory of project run:

  ```bash
  sudo user/tests/integration/run.sh
  ```

- Todo service:

  Being in root directory of project run:

  ```bash
  sudo todo/tests/integration/run.sh
  ```

### Running end2end tests

Being in root directory of project run:

```bash
sudo test/run.sh
```

## Technology stack

### User service technology stack

- Python3
- Docker
- gRPC Python
- SQLAlchemy
- PyJWT
- MariaDB (MySQL relational database management system)

### Todo service technology stack

- Python3
- Docker
- gRPC Python
- SQLAlchemy
- PyJWT
- MariaDB (MySQL relational database management system)

### Gateway API service technology stack

- C++
- Docker
- gRPC C++ with SSL
- jwt-cpp
- CMake

### End2end tests technology stack

- Python3
- Docker
- gRPC Python
- PyJWT

## Diagrams

### Deployment diagram

![Deployment diagram](/docs/diagrams/out/deployment_diagram.png?raw=true)

### Login user sequence diagram

![Login user sequence diagram](/docs/diagrams/out/login_user_sequence.png?raw=true)

### Register user sequence diagram

![Register user sequence diagram](/docs/diagrams/out/register_user_sequence.png?raw=true)

### Create todo sequence diagram

![Create todo sequence diagram](/docs/diagrams/out/create_todo_sequence.png?raw=true)

### Get todo sequence diagram

![Get todo sequence diagram](/docs/diagrams/out/get_todo_sequence.png?raw=true)

### Delete todo sequence diagram

![Delete todo sequence diagram](/docs/diagrams/out/delete_todo_sequence.png?raw=true)

### Update todo sequence diagram

![Update todo sequence diagram](/docs/diagrams/out/update_todo_sequence.png?raw=true)

### List todo sequence diagram

![List todo sequence diagram](/docs/diagrams/out/list_todo_sequence.png?raw=true)
