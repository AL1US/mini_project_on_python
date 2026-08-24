### 1. Браузер хочет получить ресурс

Например:

```text
GET /index HTTP/1.1
Host: example.com
```

Браузер знает:

```text
IP сервера: 93.184.216.34
порт: 443
протокол: HTTPS
```

Для HTTPS обычно получается:

```text
HTTP
  ↓
TLS
  ↓
TCP
  ↓
IP
  ↓
Ethernet / Wi-Fi
```

---

### 2. Пакеты приходят на сервер

Сетевая карта принимает Ethernet-кадры и передаёт их ОС.

Дальше:

```text
NIC
 ↓
Ethernet
 ↓
IP
 ↓
TCP
```

TCP-стек ОС смотрит:

> «На какой TCP-сокет предназначены эти данные?»

---

### 3. На сервере есть listening socket

Например, сервер заранее сделал:

```text
TCP socket
bind(0.0.0.0:443)
listen()
```

Получается:

```text
              SERVER
                 │
        TCP listening socket
             :443
                 │
        ждёт новые соединения
```

Он **не занимается непосредственно HTTP**.

Его задача:

> «Есть ли новый TCP-клиент, который хочет установить соединение со мной на 443 порт?»

---

### 4. Приходит новый клиент

Например:

```text
Client: 192.168.1.20:52341
Server: 93.184.216.34:443
```

TCP устанавливает соединение через handshake:

```text
Client                  Server

   SYN  ────────────────>
        <──────── SYN-ACK
   ACK  ────────────────>
```

После этого TCP-соединение существует.

И вот здесь появляется **connected socket**.

---

### 5. Listening socket создаёт connected socket

Условно:

```text
                 Server
                    │
          ┌─────────┴─────────┐
          │                   │
     listening socket     connected socket
        :443                  :443
          │                    │
     ждёт клиентов        Client A
```

Причём **локальный порт может быть тем же самым — 443**.

Например:

```text
Client A: 10.0.0.5:50001
Server:   1.2.3.4:443

Client B: 10.0.0.6:50002
Server:   1.2.3.4:443
```

Оба соединения используют серверный порт `443`.

Они различаются по **четвёрке**:

```text
(source IP,
 source port,
 destination IP,
 destination port)
```

Например:

```text
(10.0.0.5, 50001, 1.2.3.4, 443)
(10.0.0.6, 50002, 1.2.3.4, 443)
```

Поэтому сервер спокойно может иметь тысячи соединений одновременно на одном `443`.

---

### 6. А вот теперь появляется backend / HTTP-сервер

Вот это важное разделение.

TCP говорит:

> «Я установил надёжный поток байтов между клиентом и сервером».

Но TCP **не знает**, что такое:

```text
GET /index
POST /login
Content-Type: application/json
```

Это уже **HTTP**.

Поэтому поверх TCP работает HTTP-сервер / серверное приложение.

Например:

```text
                 SERVER
                    │
             TCP listening :443
                    │
              connected socket
                    │
                  TLS
                    │
                  HTTP
                    │
             backend application
                    │
              business logic
                    │
                 database
```

В Python это может быть условно:

```text
Internet
   ↓
TCP
   ↓
TLS
   ↓
HTTP server
   ↓
FastAPI
   ↓
your endpoint
   ↓
PostgreSQL
```

---

### 7. Что происходит с `GET /index`

Допустим, TCP уже установил соединение.

Браузер отправляет байты:

```text
GET /index HTTP/1.1
Host: example.com
```

TCP просто передаёт эти байты.

HTTP-сервер читает их и понимает:

```text
метод = GET
path = /index
headers = ...
```

Дальше передаёт запрос backend-приложению:

```text
GET /index
      ↓
HTTP server
      ↓
FastAPI
      ↓
@app.get("/index")
      ↓
логика приложения
```

Backend генерирует ответ:

```text
HTTP/1.1 200 OK

<html>...</html>
```

И дальше всё идёт обратно:

```text
Backend
  ↓
HTTP response
  ↓
TLS
  ↓
TCP
  ↓
IP
  ↓
NIC
  ↓
Internet
  ↓
Browser
```

---

## Вся картина целиком

Если собрать **именно серверную часть**, то получается:

```text
                    INTERNET
                       │
                       ▼
                    NIC
                       │
                 Ethernet / IP
                       │
                       ▼
                  TCP stack
                       │
              ┌────────┴────────┐
              │                 │
       listening socket    connected sockets
          :443              :443 ← Client A
                            :443 ← Client B
                            :443 ← Client C
                                  ...
                              │
                              ▼
                             TLS
                              │
                              ▼
                         HTTP server
                              │
                              ▼
                       Backend application
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                 Business            Database
                  logic
```

### Самое важное различие

Не надо представлять это как:

> **TCP socket → backend**

Лучше держать в голове:

> **TCP обеспечивает соединение и поток байтов. HTTP интерпретирует эти байты как HTTP-запрос. Backend обрабатывает HTTP-запрос и выполняет бизнес-логику.**

И ещё:

> **Listening socket не обслуживает сам HTTP-запрос.** Он нужен для приёма новых TCP-соединений. После `accept()` работа с конкретным клиентом идёт через отдельный connected socket.

Именно эта модель потом очень хорошо объясняет, **что такое Nginx, Gunicorn/Uvicorn, FastAPI, reverse proxy, worker'ы и почему один сервер может одновременно обслуживать тысячи клиентов**.
