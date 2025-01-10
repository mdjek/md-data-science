1. Вывести все директории в виде: ID, Название, Путь до корня

```sql
 WITH RECURSIVE path_q AS
  ( SELECT id,
           parent_id,
           name,
           CAST(ARRAY[name::text] AS text[]) AS path_list
   FROM file_system
   WHERE parent_id IS NULL
     AND TYPE = 'DIR'
   UNION ALL SELECT f.id,
                    f.parent_id,
                    f.name,
                    array_append(p.path_list, f.name::text)
   FROM file_system f
   JOIN path_q p ON f.parent_id = p.id
   WHERE f.TYPE = 'DIR')

SELECT id,
       name,
       array_to_string(path_list, '/') AS full_path
FROM path_q
ORDER BY path_list;
```

2. Для каждой директории посчитать объем занимаемого места на диске (с учетом всех вложенных папок): ID, Название, Путь до корня, total_size.

```sql
 WITH RECURSIVE path_q AS
  ( SELECT id,
           parent_id,
           name,
           CAST(ARRAY[name::text] AS text[]) AS path_list
   FROM file_system
   WHERE parent_id IS NULL
     AND TYPE = 'DIR'
   UNION ALL SELECT f.id,
                    f.parent_id,
                    f.name,
                    array_append(p.path_list, f.name::text)
   FROM file_system f
   JOIN path_q p ON f.parent_id = p.id
   WHERE f.TYPE = 'DIR'),
                dir_sizes AS
  ( SELECT COALESCE(fs.parent_id, fs.id) AS dir_id,
           SUM(fs.file_size) AS total_size
   FROM file_system fs
   WHERE fs.TYPE = 'FILE'
   GROUP BY COALESCE(fs.parent_id, fs.id))
SELECT p.id,
       p.name,
       array_to_string(p.path_list, '/') AS full_path,
       COALESCE(d.total_size, 0) AS total_size
FROM path_q p
LEFT JOIN dir_sizes d ON d.dir_id = p.id
ORDER BY p.path_list;
```

3. Добавить в запрос: сколько процентов директория занимает места относительно всех среди своих соседей (siblings): ID, Название, Путь до корня, total_size, ratio.

```sql
 WITH RECURSIVE path_q AS
  ( SELECT id,
           parent_id,
           name,
           CAST(ARRAY[name::text] AS text[]) AS path_list
   FROM file_system
   WHERE parent_id IS NULL
     AND TYPE = 'DIR'
   UNION ALL SELECT f.id,
                    f.parent_id,
                    f.name,
                    array_append(p.path_list, f.name::text)
   FROM file_system f
   JOIN path_q p ON f.parent_id = p.id
   WHERE f.TYPE = 'DIR'),
                dir_sizes AS
  ( SELECT COALESCE(fs.parent_id, fs.id) AS dir_id,
           SUM(fs.file_size) AS total_size
   FROM file_system fs
   WHERE fs.TYPE = 'FILE'
   GROUP BY COALESCE(fs.parent_id, fs.id))
SELECT p.id,
       p.name,
       array_to_string(p.path_list, '/') AS full_path,
       COALESCE(d.total_size, 0) AS total_size,
       ROUND( CASE WHEN SUM(COALESCE(d.total_size, 0)) OVER (PARTITION BY p.parent_id) = 0 THEN 0 ELSE COALESCE(d.total_size, 0) * 100.0 / SUM(COALESCE(d.total_size, 0)) OVER (PARTITION BY p.parent_id) END, 2 ) AS size_ratio
FROM path_q p
LEFT JOIN dir_sizes d ON d.dir_id = p.id
ORDER BY p.path_list;
```
