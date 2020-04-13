# pg-vacuum
Managing PostgreSQL vacuums/autovacuums.

## Features

This little tool will hopefully make managing the craziness that Postgres autovacuum is a little easier.


### Show current vacuums/autovacuums
It will show you how long the vacuums are running for and how much is left to do.

```
$ pgvacuum --database=postgres://localhost/db
```

### Show progress of vacuums/autovacuums

```
$ pgvacuum --database=postgres://localhost/db --progress
```

### Enable/disable autovacuum on a table

```
$ pgvacuum --database=postgres://localhost/db --table=my_table --disable
$ pgvacuum --database=postgres://localhost/db --table=my_table --enable
```

### Show table settings

Show what current settings are set on the table.

```
$ pgvacuum --database=postgres://localhost/db --table=my_table
```

### Terminate the autovacuums

Ok, you've had enough of it.

```
$ pgvacuum --database=postgres://localhost/db --kill=1234
```

where `1234` is the PID of the vacuum/autovacuum process.

