
langs: [EN](#EN), [RU](#RU)

# Project Description
<a id="EN"></a>
The microservice allows versioning of JSON objects.


## Main Tasks
The main tasks of the module are to provide the following capabilities for the user:

- register REF
  - after registration, receive back ref_hash
- register versions of CONTENT by REF
  - receive a content version (VID) for each field in the content
- receive the latest version of the content by REF
- receive a specific version of the content by VID

Any document can serve as a document: a primary source document (dpi), tpi, brand, site, instagram, etc.

REF and CONTENT serve as parameters for registering documents.

REF can be registered separately from CONTENT at a separate endpoint.

# Hashing
CONTENT is hashed, the result goes into the COMMON_HASH variable inside the program, and at the output of the program into the CONTENT_HASH variable

Each key-value pair inside the content is also hashed and added to the CONTENT_HASHES array.

## Hashing Algorithm
sha256
To calculate the hash for two variables: key-value; two strings are concatenated, and a hash is calculated for the resulting string.

[DATABASE CONFIG](#DATABASE)

# Описание проекта
<a id="RU"></a>
Микросервис позоволяет вести версионирование JSON-объектов.

## Основные задачи
Основными задачами модуля является обеспечение следующих возможностей для пользователя:
- регистрировать *REF*
	- после регистрации получать обратно *ref_hash*
- регистрировать версии *CONTENT*'а по *REF*
	- получать версию контента (*VID*) по каждому полю в контенте
- получать последнюю версию контента по *REF*
- получать определенную версию контента по *VID*


В качестве документа может выступать любой документ: документ первоисточника(*dpi*), *tpi*, *brand*, *site*, *instagram* и т.д.

В качестве параметров для регистрации документов выступают *REF* и *CONTENT*.

REF можно зарегистрировать отдельно от CONTENT в отдельном эндпоинте.

## Хеширование
*CONTENT* хешируется, результат попадает в переменную *COMMON_HASH* внутри программы, а на выходе из программы в переменную *CONTENT_HASH*

Также хешируется каждая пара ключ-значение внутри контента и добавляется в массив *CONTENT_HASHES*.

### Алгоритм хеширования
**sha256**
Для расчета хеша для двух переменных: ключ-значения; две строки конкатенируются и для результурующей строки вычисляется хеш.
# DATABASE CONFIG
<a id="DATABASE"></a>
```bash
docker run --restart unless-stopped --name scylla-db -d -p 7004:7000 -p 9046:9042 scylladb/scylla:5.1
```

```cql
CREATE KEYSPACE IF NOT EXISTS dev  
    WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'replication_factor' : '1' };  

create table if not exists dev.id_record  
(  
    id         bigint,  
    created_at timestamp,  
    ref        text,  
    ref_hash   text,
    primary key (id)
);
  
create index IF NOT EXISTS ref  
    on dev.id_record (ref);  
  
create index IF NOT EXISTS ref_hash  
    on dev.id_record (ref_hash);  

```

```cql
create table dev.vid_record 
(  
    id             bigint,  
    vid            bigint,  
    common_hash    text,  
    content        text,  
    content_hashes text,  
    created_at     timestamp,  
    evolution      text,  
    ref            text,
    primary key (id, vid)
) with clustering order by (vid desc);
  
create index IF NOT EXISTS common_hash  
    on dev.vid_record (common_hash);
```
