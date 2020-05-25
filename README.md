# pg-vacuum
Managing PostgreSQL vacuums/autovacuums. This little tool will hopefully make managing the craziness that Postgres autovacuum is a little easier.

## Features

### Show current vacuums/autovacuums
It will show you how long the vacuums are running for and how much is left to do.

```bash
$ pgvacuum --database=postgres://localhost/db

+-------+--------------------------------------+----------------------------------+----------------+
|  PID  |                Query                 |             Started              |    Duration    |
+-------+--------------------------------------+----------------------------------+----------------+
| 13368 |  autovacuum: VACUUM public.drivers   | 2020-04-16 14:19:17.289047+00:00 | 0:53:24.403651 |
| 80617 | autovacuum: VACUUM public.old_carts  | 2020-04-16 14:16:17.484278+00:00 | 0:56:24.208420 |
| 92409 | autovacuum: VACUUM public.table_one_ | 2020-04-16 13:21:37.663504+00:00 | 1:51:04.029194 |
| 79790 |  autovacuum: VACUUM public.devices   | 2020-04-16 14:44:18.791010+00:00 | 0:28:22.901688 |
| 97037 |   autovacuum: VACUUM public.users    | 2020-04-16 12:21:10.163915+00:00 | 2:51:31.528783 |
+-------+--------------------------------------+----------------------------------+----------------+
```


### Show progress of vacuums/autovacuums

```bash
$ pgvacuum --database=postgres://localhost/db --progress

+-------+------------+-------------------+----------+----------------------------------+----------------+
|  PID  |   Table    |       Phase       | Progress |             Started              |    Duration    |
+-------+------------+-------------------+----------+----------------------------------+----------------+
| 92409 | table_one_ | vacuuming indexes |   100    | 2020-04-16 13:21:37.663504+00:00 | 1:54:48.656212 |
| 97037 |   users    | vacuuming indexes |   100    | 2020-04-16 12:21:10.163915+00:00 | 2:55:16.155801 |
| 79790 |  devices   | vacuuming indexes |   100    | 2020-04-16 14:44:18.791010+00:00 | 0:32:07.528706 |
| 13368 |  table_t   | vacuuming indexes |   100    | 2020-04-16 14:19:17.289047+00:00 | 0:57:09.030669 |
| 80617 | old_carts  | vacuuming indexes |   100    | 2020-04-16 14:16:17.484278+00:00 | 1:00:08.835438 |
+-------+------------+-------------------+----------+----------------------------------+----------------+
```

### Enable/disable autovacuum on a table

```bash
# Disable the autovacuum on this table
$ pgvacuum --database=postgres://localhost/db --table=my_table --disable

# Enable the autovacuum on this table
$ pgvacuum --database=postgres://localhost/db --table=my_table --enable
```

### Show table settings

Show what current settings are set on the table.

```bash
$ pgvacuum --database=postgres://localhost/db --table=my_table

+--------------------------------+-----------+
|            Setting             |   Value   |
+--------------------------------+-----------+
|   autovacuum_freeze_max_age    | 500000000 |
| autovacuum_vacuum_scale_factor |    0.02   |
|       autovacuum_enabled       |   false   |
+--------------------------------+-----------+
```

### Show current autovacuum settings

Show current database autovacuum settings.

```bash
pgvacuum --database=postgres://localhost/src --settings

+---------------------------------+-----------+
|             Setting             |   Value   |
+---------------------------------+-----------+
|   autovacuum_vacuum_cost_delay  |    2ms    |
|   autovacuum_vacuum_cost_limit  |    200    |
|        autovacuum_naptime       |    1min   |
|  autovacuum_vacuum_scale_factor |    0.2    |
| autovacuum_analyze_scale_factor |    0.1    |
|    autovacuum_freeze_max_age    | 200000000 |
|           track_counts          |     on    |
+---------------------------------+-----------+
```


### Terminate the autovacuums

Ok, you've had enough of it.

```bash
$ pgvacuum --database=postgres://localhost/db --kill=1234
```

where `1234` is the PID of the vacuum/autovacuum process.


### Arguments
1. `--database` (required), DSN or `postgres://` URL for the database,
2. `--progress`, show the progress of running vacuums,
3. `--table`, show settings for this table,
4. `--enable/disable`, to be used in conjunction with `--table` to enable/disable autovacuum on it,
5. `--kill`, kill the autovacuum/vacuum with this PID.

