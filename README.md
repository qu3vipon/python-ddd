# [WIP] Python Domain-Driven-Design(DDD) Example

# Intro
I have adopted the DDD pattern for my recent FastAPI project.
DDD makes it easier to implement complex domain problems.
Improved readability and easier modification of code has resulted in significant productivity gains.
As a result, stable service and project management has become possible.
I'm very satisfied with it, so I want to share this experience.

## Why DDD?
Using DDD makes it easy to maintain collaboration with domain experts, not only engineers.
- It is possible to prevent the mental model and the actually implemented software from being dualized.
- Business logic is easy to manage.
- Infrastructure change is flexible.


## Objective
Let's create a simple hotel reservation system and see how each component of DDD is implemented.

# Implementation
## ERD
> NOTES: The diagram below represents only the database tables.

![erd](./docs/image/erd.png)

## Bounded Context

![bounded-context](./docs/image/bounded-context.png)
