import ctypes

import dbe

import ibis.common.exceptions as com
import ibis.config as cf
from ibis.config import options
from ibis.omniscidb.client import EXECUTION_TYPE_CURSOR, OmniSciDBClient
from ibis.omniscidb.compiler import compiles, dialect, rewrites  # noqa: F401

ctypes.CDLL('libDBEngine.so', mode=ctypes.RTLD_GLOBAL)


def compile(expr, params=None):
    """
    Force compilation of expression as though it were an expression depending
    on OmniSciDB. Note you can also call expr.compile()

    Returns
    -------
    compiled : string
    """
    from ibis.omniscidb.compiler import to_sql

    return to_sql(expr, dialect.make_context(params=params))


def verify(expr, params=None):
    """
    Determine if expression can be successfully translated to execute on
    OmniSciDB
    """
    try:
        compile(expr, params=params)
        return True
    except com.TranslationError:
        return False


def connect(
    uri=None,
    user=None,
    password=None,
    host=None,
    port=6274,
    database=None,
    protocol='binary',
    session_id=None,
    execution_type=EXECUTION_TYPE_CURSOR,
):
    """Create a OmniSciDBClient for use with Ibis

    Parameters could be

    :param uri: str
    :param user: str
    :param password: str
    :param host: str
    :param port: int
    :param database: str
    :param protocol: str
    :param session_id: str
    :param execution_type: int
    Returns
    -------
    OmniSciDBClient

    """
    client = OmniSciDBClient(
        uri=uri,
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        protocol=protocol,
        session_id=session_id,
        execution_type=execution_type,
    )

    if options.default_backend is None:
        options.default_backend = client

    with cf.config_prefix('sql'):
        k = 'default_limit'
        cf.set_option(k, None)

    return client


def engine(uri):
    return dbe.PyDbEngine(uri)
