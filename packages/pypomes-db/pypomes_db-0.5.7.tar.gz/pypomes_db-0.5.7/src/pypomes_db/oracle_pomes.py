# noinspection DuplicatedCode
from logging import Logger
from oracledb import Connection, connect, init_oracle_client
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .db_common import (
    _DB_CONN_DATA,
    _assert_query_quota, _db_get_params, _db_log, _db_except_msg
)
from .db_pomes import db_bulk_insert as db_bulk_insert_to
from .db_pomes import db_update_lob as db_update_lob_to


def db_connect(errors: list[str],
               logger: Logger) -> Connection:
    """
    Obtain and return a connection to the database, or *None* if the connection could not be obtained.

    :param errors: incidental error messages
    :param logger: optional logger
    :return: the connection to the database
    """
    # initialize the return variable
    result: Connection | None = None

    # retrieve the connection parameters
    name, user, pwd, host, port = _db_get_params("oracle")

    # obtain a connection to the database
    err_msg: str | None = None
    try:
        result = connect(service_name=name,
                         host=host,
                         port=port,
                         user=user,
                         password=pwd)
        # make sure the connection is not in autocommit mode
        result.autocommit = False
    except Exception as e:
        err_msg = _db_except_msg(exception=e,
                                 engine="oracle")

    # log the results
    _db_log(logger=logger,
            err_msg=err_msg,
            errors=errors,
            query_stmt=f"Connecting to '{name}' at '{host}'")

    return result


def db_select_all(errors: list[str],
                  sel_stmt: str,
                  where_vals: tuple,
                  require_min: int,
                  require_max: int,
                  conn: Connection,
                  logger: Logger) -> list[tuple]:
    """
    Search the database and return all tuples that satisfy the *sel_stmt* search command.

    The command can optionally contain search criteria, with respective values given
    in *where_vals*. The list of values for an attribute with the *IN* clause must be contained
    in a specific tuple. If not positive integers, *require_min* and *require_max* are ignored.
    If the search is empty, an empty list is returned.

    :param errors: incidental error messages
    :param sel_stmt: SELECT command for the search
    :param where_vals: the values to be associated with the search criteria
    :param require_min: optionally defines the minimum number of tuples to be returned
    :param require_max: optionally defines the maximum number of tuples to be returned
    :param conn: optional connection to use (obtains a new one, if not specified)
    :param logger: optional logger
    :return: tuple containing the search result, [] if the search was empty, or None if there was an error
    """
    # initialize the return variable
    result: list[tuple] = []

    # make sure to have a connection
    curr_conn: Connection = conn or db_connect(errors=errors,
                                               logger=logger)

    if isinstance(require_max, int) and require_max > 0:
        sel_stmt: str = f"{sel_stmt} FETCH NEXT {require_max} ROWS ONLY"

    err_msg: str | None = None
    try:
        # obtain a cursor and perform the operation
        with curr_conn.cursor() as cursor:
            # execute the query
            cursor.execute(statement=sel_stmt,
                           parameters=where_vals)
            # obtain the number of tuples returned
            count: int = cursor.rowcount

            # has the query quota been satisfied ?
            if _assert_query_quota(errors=errors,
                                   query=sel_stmt,
                                   where_vals=where_vals,
                                   count=count,
                                   require_min=require_min,
                                   require_max=require_max):
                # yes, retrieve the returned tuples
                rows: list = cursor.fetchall()
                result = [tuple(row) for row in rows]
        # commit the transaction
        curr_conn.commit()
    except Exception as e:
        curr_conn.rollback()
        err_msg = _db_except_msg(exception=e,
                                 engine="oracle")
    finally:
        # close the connection, if locally acquired
        if not conn:
            curr_conn.close()

    # log the results
    _db_log(logger=logger,
            err_msg=err_msg,
            errors=errors,
            query_stmt=sel_stmt,
            bind_vals=where_vals)

    return result


def db_bulk_insert(errors: list[str],
                   insert_stmt: str,
                   insert_vals: list[tuple],
                   conn: Connection,
                   logger: Logger) -> int:
    """
    Insert the tuples, with values defined in *insert_vals*, into the database.

    The binding must be done by position. Thus, the *VALUES* clause in *insert_stmt*
    must contain as many ':n' placeholders as there are elements in the tuples found in the
    list provided in *insert_vals*, where 'n' is the 1-based position of the data in the tuple.

    :param errors: incidental error messages
    :param insert_stmt: the INSERT command
    :param insert_vals: the list of values to be inserted
    :param conn: optional connection to use (obtains a new one, if not specified)
    :param logger: optional logger
    :return: the number of inserted tuples, or None if an error occurred
    """
    # initialize the return variable
    result: int | None = None

    # make sure to have a connection
    curr_conn: Connection = conn or db_connect(errors=errors,
                                               logger=logger)

    err_msg: str | None = None
    try:
        # obtain a cursor and perform the operation
        with curr_conn.cursor() as cursor:
            cursor.executemany(statement=insert_stmt,
                               parameters=insert_vals)
            result = len(insert_vals)
        curr_conn.commit()
    except Exception as e:
        curr_conn.rollback()
        err_msg = _db_except_msg(exception=e,
                                 engine="oracle")
    finally:
        # close the connection, if locally acquired
        if not conn:
            curr_conn.close()

    # log the results
    _db_log(logger=logger,
            err_msg=err_msg,
            errors=errors,
            query_stmt=insert_stmt,
            bind_vals=insert_vals[0])

    return result


def db_bulk_copy(errors: list[str],
                 sel_stmt: str,
                 insert_stmt: str,
                 target_engine: str,
                 batch_size: int,
                 where_vals: tuple,
                 target_conn: Any,
                 conn: Connection,
                 logger: Logger) -> int:
    """
    Bulk copy data from a Oracle database to another database.

    The destination database brand must be in the list of databases configured and supported by this package.

    :param errors: incidental error messages
    :param sel_stmt: SELECT command for the search
    :param insert_stmt: the insert statement to use for bulk-inserting
    :param target_engine: the destination database engine type
    :param batch_size: number of tuples in the batch, or 0 or None for no limit
    :param where_vals: the values to be associated with the search criteria
    :param target_conn: the connection to the destination database
    :param conn: optional connection to use (obtains a new one, if not specified)
    :param logger: optional logger
    :return: number of tuples effectively copied
    """
    # initialize the return variable
    result: int | None = None

    # make sure to have a connection
    curr_conn: Connection = conn or db_connect(errors=errors,
                                               logger=logger)

    err_msg: str | None = None
    try:
        with curr_conn.cursor() as cursor:

            # execute the query
            cursor.execute(statement=sel_stmt,
                           parameters=where_vals)

            # fetch rows in batches/all rows
            result = 0
            op_errors: list[str] = []
            rows: list[tuple]
            if batch_size:
                rows = cursor.fetchmany(size=batch_size)
            else:
                rows = cursor.fetchall()
            while rows:
                result += db_bulk_insert_to(errors=op_errors,
                                            insert_stmt=insert_stmt,
                                            insert_vals=rows,
                                            engine=target_engine,
                                            conn=target_conn,
                                            logger=logger) or 0
                # errors ?
                if op_errors:
                    # yes, register them and abort the operation
                    errors.extend(op_errors)
                    break
                if not batch_size:
                    break
                rows = cursor.fetchmany(batch_size)

        # commit the source and target transactions
        curr_conn.commit()
        if target_conn:
            target_conn.commit()
    except Exception as e:
        err_msg = _db_except_msg(exception=e,
                                 engine="oracle")
        curr_conn.rollback()
        if target_conn:
            target_conn.rollback()
    finally:
        # close the connection, if locally acquired
        if not conn:
            curr_conn.close()

    # log the results
    _db_log(logger=logger,
            err_msg=err_msg,
            errors=errors,
            query_stmt=sel_stmt,
            bind_vals=where_vals)

    return result


def db_migrate_lobs(errors: list[str],
                    lob_table: str,
                    lob_column: str,
                    pk_columns: list[str],
                    target_engine: str,
                    where_clause: tuple,
                    temp_file: str | Path,
                    chunk_size: int,
                    target_table: str,
                    target_column: str,
                    target_conn: Any,
                    conn: Connection,
                    logger: Logger) -> int:
    """
    Migrate large binary objects (LOBs) from an Oracle database to another database.

    The destination database must be in the list of databases configured and supported by this package.
    One or more columns making up a primary key, or a unique row identifier, must exist on *lob_table*,
    and be provided in *pk_columns*. It is assumed that the primary key columns have the same name,
    and are of equivalent types, in both the origin and the destination database.
    If *temp_file* is not provided, a plataform-specific temporary file is used.

    :param errors: incidental error messages
    :param lob_table: the table holding the LOBs
    :param lob_column: the column holding the LOB
    :param pk_columns: columns making up a primary key, or a unique identifier for the tuple
    :param target_engine: the destination database engine type
    :param where_clause: the criteria for tuple selection
    :param temp_file: temporary file to use (a file object or a valid file path)
    :param chunk_size: size in bytes of the data chunk to read/write, or 0 or None for no limit
    :param target_table: the table to write the lob to (defaults to the source table)
    :param target_column: the column to write the lob to (defaults to the source column)
    :param target_conn: the connection to the destination database
    :param conn: optional connection to use (obtains a new one, if not specified)
    :param logger: optional logger
    :return: number of LOBs effectively migrated
    """
    # initialize the return variable
    result: int = 0

    # make sure to have a connection
    curr_conn: Connection = conn or db_connect(errors=errors,
                                               logger=logger)

    # make sure to have a target table
    if not target_table:
        target_table = lob_table

    # make sure to have a temporary file
    lob_file: Any
    if temp_file is None:
        lob_file = NamedTemporaryFile("wb")
    elif isinstance(temp_file, str | Path):
        lob_file = Path(temp_file)
    else:
        lob_file = temp_file

    # normalize the chunk size
    if not chunk_size:
        chunk_size = -1

    # buid the query
    pks: str = ", ".join(pk_columns)
    sel_stmt: str = f"SELECT {pks}, {lob_column} FROM {lob_table}"
    if where_clause:
        sel_stmt += f" WHERE {where_clause}"
    blob_index: int = len(pk_columns)

    err_msg: str | None = None
    try:
        with curr_conn.cursor() as cursor:

            # execute the query
            cursor.execute(statement=sel_stmt)

            # fetch rows
            for row in cursor:

                # retrieve the values of the primary key columns (leave blob column out)
                pk_vals: tuple = tuple([row[inx] for inx in range(blob_index)])

                # access the blob in chunks and write it to file
                blob: Any = row[blob_index]
                with lob_file.open(mode="wb") as file:
                    blob_data: bytes = blob.read(chunk_size)
                    while blob_data:
                        file.write(blob_data)
                        blob_data = blob.read(chunk_size)

                # send blob to the destination database
                op_errors: list[str] = []
                db_update_lob_to(errors=op_errors,
                                 lob_table=target_table,
                                 lob_column=target_column,
                                 lob_file=lob_file,
                                 chunk_size=chunk_size,
                                 pk_columns=pk_columns,
                                 pk_vals=pk_vals,
                                 engine=target_engine,
                                 conn=target_conn,
                                 logger=logger)
                # errors ?
                if op_errors:
                    # yes, register them
                    errors.extend(op_errors)
                else:
                    # no, increment the LOB migration counter
                    result += 1

        # commit the source and target transactions
        curr_conn.commit()
        target_conn.commit()
    except Exception as e:
        err_msg = _db_except_msg(exception=e,
                                 engine="oracle")
        curr_conn.rollback()
        if target_conn:
            target_conn.rollback()
    finally:
        # close the connection, if locally acquired
        if not conn:
            curr_conn.close()

    # log the results
    _db_log(logger=logger,
            err_msg=err_msg,
            errors=errors,
            query_stmt=(f"{result} LOBs migrated, "
                        f"from oracle at {lob_table}.{lob_column} "
                        f"to {target_engine} at {target_table}.{target_column}"))

    return result


def db_update_lob(errors: list[str],
                  lob_table: str,
                  lob_column: str,
                  pk_columns: list[str],
                  pk_vals: tuple,
                  lob_file: str | Path,
                  chunk_size: int,
                  conn: Connection,
                  logger: Logger) -> None:
    """
    Update a large binary objects (LOB) in the given table and column.

    :param errors: incidental error messages
    :param lob_table: the table to be update with the new LOB
    :param lob_column: the column to be updated with the new LOB
    :param pk_columns: columns making up a primary key, or a unique identifier for the tuple
    :param pk_vals: values with which to locate the tuple to be updated
    :param lob_file: file holding the LOB (a file object or a valid path)
    :param chunk_size: size in bytes of the data chunk to read/write, or 0 or None for no limit
    :param conn: optional connection to use (obtains a new one, if not specified)
    :param logger: optional logger
    """
    # make sure to have a connection
    curr_conn: Connection = conn or db_connect(errors=errors,
                                               logger=logger)

    # make sure to have a data file
    data_file: Path = Path(lob_file) if isinstance(lob_file, str | Path) else lob_file

    # normalize the chunk size
    if not chunk_size:
        chunk_size = -1

    # build the UPDATE query
    where_clause: str = " AND ".join([f"{column} = :{inx}"
                                      for column, inx in enumerate(iterable=pk_columns,
                                                                   start=2)])
    update_stmt: str = (f"UPDATE {lob_table} "
                        f"SET {lob_column} = :1 "
                        f"WHERE {where_clause}")

    err_msg: str | None = None
    try:
        # obtain a cursor and execute the operation
        with curr_conn.cursor() as cursor:

            # retrieve the lob data from file in chunks and write to the file
            lob_data : bytes
            with data_file.open("rb") as file:
                lob_data = file.read(chunk_size)
                while lob_data:
                    cursor.execute(statement=update_stmt,
                                   parameters=(lob_data, *pk_vals))
                    lob_data = file.read(chunk_size)

        # commit the transaction
        curr_conn.commit()
    except Exception as e:
        curr_conn.rollback()
        err_msg = _db_except_msg(exception=e,
                                 engine="oracle")
    finally:
        # close the connection, if locally acquired
        if not conn:
            curr_conn.close()

    # log the results
    _db_log(logger=logger,
            err_msg=err_msg,
            errors=errors,
            query_stmt=update_stmt,
            bind_vals=pk_vals)


def db_execute(errors: list[str],
               exc_stmt: str,
               bind_vals: tuple,
               conn: Connection,
               logger: Logger) -> int:
    """
    Execute the command *exc_stmt* on the database.

    This command might be a DML ccommand modifying the database, such as
    inserting, updating or deleting tuples, or it might be a DDL statement,
    or it might even be an environment-related command.
    The optional bind values for this operation are in *bind_vals*.
    The value returned is the value obtained from the execution of *exc_stmt*.
    It might be the number of inserted, modified, or deleted tuples,
    ou None if an error occurred.

    :param errors: incidental error messages
    :param exc_stmt: the command to execute
    :param bind_vals: optional bind values
    :param conn: optional connection to use (obtains a new one, if not specified)
    :param logger: optional logger
    :return: the return value from the command execution
    """
    # initialize the return variable
    result: int | None = None

    # make sure to have a connection
    curr_conn: Connection = conn or db_connect(errors=errors,
                                               logger=logger)

    err_msg: str | None = None
    try:
        # obtain a cursor and execute the operation
        with curr_conn.cursor() as cursor:
            cursor.execute(statement=exc_stmt,
                           parameters=bind_vals)
            result = cursor.rowcount
        # commit the transaction
        curr_conn.commit()
    except Exception as e:
        curr_conn.rollback()
        err_msg = _db_except_msg(exception=e,
                                 engine="oracle")
    finally:
        # close the connection, if locally acquired
        if not conn:
            curr_conn.close()

    # log the results
    _db_log(logger=logger,
            err_msg=err_msg,
            errors=errors,
            query_stmt=exc_stmt,
            bind_vals=bind_vals)

    return result


# TODO: see https://python-oracledb.readthedocs.io/en/latest/user_guide/plsql_execution.html
# noinspection PyUnusedLocal
def db_call_function(errors: list[str],
                     func_name: str,
                     func_vals: tuple,
                     conn: Connection,
                     logger: Logger) -> list[tuple]:
    """
    Execute the stored function *func_name* in the database, with the parameters given in *func_vals*.

    :param errors: incidental error messages
    :param func_name: name of the stored function
    :param func_vals: parameters for the stored function
    :param conn: optional connection to use (obtains a new one, if not specified)
    :param logger: optional logger
    :return: the data returned by the function
    """
    # initialize the return variable
    result: list[tuple] = []

    return result


# TODO: see https://python-oracledb.readthedocs.io/en/latest/user_guide/plsql_execution.html
def db_call_procedure(errors: list[str],
                      proc_name: str,
                      proc_vals: tuple,
                      conn: Connection,
                      logger: Logger) -> list[tuple]:
    """
    Execute the stored procedure *proc_name* in the database, with the parameters given in *proc_vals*.

    :param errors: incidental error messages
    :param proc_name: name of the stored procedure
    :param proc_vals: parameters for the stored procedure
    :param conn: optional connection to use (obtains a new one, if not specified)
    :param logger: optional logger
    :return: the data returned by the procedure
    """
    # initialize the return variable
    result: list[tuple] = []

    # make sure to have a connection
    curr_conn: Connection = conn or db_connect(errors=errors,
                                               logger=logger)

    # execute the stored procedure
    err_msg: str | None = None
    try:
        # obtain a cursor and perform the operation
        with curr_conn.cursor() as cursor:
            cursor.callproc(name=proc_name,
                            parameters=proc_vals)

            # retrieve the returned tuples
            result = list(cursor)
        # commit the transaction
        curr_conn.commit()
    except Exception as e:
        curr_conn.rollback()
        err_msg = _db_except_msg(exception=e,
                                 engine="oracle")
    finally:
        # close the connection, if locally acquired
        if not conn:
            curr_conn.close()

    # log the results
    _db_log(logger=logger,
            err_msg=err_msg,
            errors=errors,
            query_stmt=proc_name,
            bind_vals=proc_vals)

    return result

__is_initialized: str | None = None

def initialize(errors: list[str],
               logger: Logger) -> bool:
    """
    Prepare the oracle engine to access the database throught the installed client software.

    :param errors: incidental error messages
    :param logger: optional logger
    :return: False if an error happened, True otherwise
    """
    # initialize the return variable
    result: bool = True

    global __is_initialized
    if not __is_initialized:
        err_msg: str | None = None
        client: str = _DB_CONN_DATA["oracle"]["client"]
        try:
            init_oracle_client(client)
            __is_initialized = True
        except Exception as e:
            result = False
            err_msg = _db_except_msg(exception=e,
                                     engine="oracle")
        # log the results
        _db_log(logger=logger,
                err_msg=err_msg,
                errors=errors,
                query_stmt="Initializing the client")

    return result
