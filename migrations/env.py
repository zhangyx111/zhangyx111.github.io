import logging
import sys
from logging.config import fileConfig
from pathlib import Path

from flask import current_app

from alembic import context

# 添加项目根目录到Python模块搜索路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
alembic_ini_path = Path(config.config_file_name) if config.config_file_name else None
if alembic_ini_path and alembic_ini_path.exists():
    fileConfig(alembic_ini_path)
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    # 从alembic.ini配置中获取数据库URL
    url = config.get_main_option("sqlalchemy.url")
    if url is None:
        raise ValueError("数据库URL未在alembic.ini中配置")
    return url.replace('%', '%%')


def check_database_connection():
    """检查数据库连接是否正常"""
    try:
        engine = get_engine()
        connection = engine.connect()
        # 执行简单的查询测试连接
        connection.execute("SELECT 1")
        connection.close()
        logger.info("数据库连接测试成功")
        return True
    except Exception as e:
        logger.error(f"数据库连接测试失败: {str(e)}")
        return False


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# 导入模型模块以获取MetaData
from app.models import db
target_metadata = db.metadata


def get_metadata():
    return target_metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    
    # 检查数据库连接
    if not check_database_connection():
        logger.error("数据库连接失败，无法继续迁移")
        raise Exception("数据库连接失败，请检查数据库配置")

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            logger.info("开始执行数据库迁移...")
            try:
                context.run_migrations()
                logger.info("数据库迁移成功完成")
            except Exception as e:
                logger.error(f"数据库迁移失败: {str(e)}")
                raise


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
