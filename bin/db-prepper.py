#!/usr/bin/env python

import argparse
import logging
import logging.handlers
import os
import os.path
import shutil

# A list of valid environment
ENVIRONMENT = ['ATS', 'BGK', 'BNK', 'CMS', 'CNT', 'CQY', 'DBG', 'ECS', 'EMS', 'FRP',
               'HBF', 'HGN', 'KVN', 'LTI', 'NED', 'OTP', 'PGC', 'PGL', 'PTP', 'SER', 'SKG', 'WLH']


def init_logging():
    '''
    Initialize logger
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    c = logging.StreamHandler()
    c_formatter = logging.Formatter(fmt='%(message)s')
    c.setFormatter(c_formatter)
    c.setLevel(logging.INFO)

    f = logging.FileHandler('db-prepper.log')
    f_formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(message)s')
    f.setFormatter(f_formatter)
    f.setLevel(logging.INFO)

    logger.addHandler(c)
    logger.addHandler(f)
    return logger


def is_environment_valid(environment):
    '''
    '''
    try:
        ENVIRONMENT.index(environment.upper())
        return True
    except ValueError:
        logging.error('%s is not a valid environment name', environment)
        return False


def directory_exists(directory):
    '''
    Returns True when the given directory exists
    '''
    logging.info('Checking if %s exists ...', directory)
    if os.path.isdir(directory):
        logging.info('OK')
        return True

    logging.info('The directory %s does not exist', directory)
    return False


def create_directory(directory):
    '''
    Creates a new directory if it does not exist
    '''
    if not directory_exists(directory):
        try:
            logging.info('Create a new directory %s ...', directory)
            os.mkdir(directory)
            logging.info('OK')
        except OSError:
            logging.fatal('Failed to create a new directory %s',
                          directory)
            return False
    return True


def file_exists(infile):
    '''
    Returns True when the given file exists
    '''
    logging.info('Checking if %s exists ...', infile)
    if os.path.isfile(infile):
        logging.info('OK')
        return True

    logging.info('The file %s does not exist', infile)
    return False


def prerequisites_exists(database_path, environment):
    '''
    Each database package needs the following files and directories:

    - Archives (directory)
      CMS and ECS have additional pre-requisites

      For CMS:
      DB_CMS/POWLIGHT.cfg
      DB_CMS/POWMXD.cfg

      For ECS:
      DB_ECS/ECS.cfg

    - dac_DB_xxx (directory)
    - dac_DB_xxx/xxx/ScsDacCtrt.cfg (file)

    - Database/xml_DB_xxx (directory)
    - Database/classlist_xxx.txt (file)
    '''

    logging.info('Checking pre-requisites for %s environment ...', environment)

    archives_dir = '%s/Archives/DB_%s' % (database_path, environment)
    if not directory_exists(archives_dir):
        return False

    if environment == 'CMS':
        powlight_cfg = '%s/POWLIGHT.cfg' % (archives_dir)
        if not file_exists(powlight_cfg):
            return False
        powmxd_cfg = '%s/POWMXD.cfg' % (archives_dir)
        if not file_exists(powmxd_cfg):
            return False
    elif environment == 'ECS':
        ecs_cfg = '%s/ECS.cfg' % (archives_dir)
        if not file_exists(ecs_cfg):
            return False

    dac_dir = '%s/dac_DB_%s' % (database_path, environment)
    if not directory_exists(dac_dir):
        return False

    concentrator = '%s/dac_DB_%s/%s/ScsDacCtrt.cfg' % (
        database_path, environment, environment)
    if not file_exists(concentrator):
        return False

    xml_dir = '%s/Database/xml_DB_%s' % (database_path, environment)
    if not directory_exists(xml_dir):
        return False

    classlist = '%s/Database/classlist_%s.txt' % (
        database_path, environment)
    if not file_exists(classlist):
        return False

    logging.info('All pre-requisites for %s environment ... OK', environment)
    return True


def create_export_directory(directory):
    '''
    '''
    logging.info(
        'Creating export directory for %s environment ...', directory)

    if not create_directory(directory):
        return False

    archives_dir = '%s/Archives' % (directory)
    if not create_directory(archives_dir):
        return False

    if directory == 'CMS':
        powlight_dir = '%s/CMST_POWLIGHT' % (archives_dir)
        if not create_directory(powlight_dir):
            return False
        powmxd_dir = '%s/CMST_POWMXD' % (archives_dir)
        if not create_directory(powmxd_dir):
            return False
    elif directory == 'ECS':
        ecs_dir = '%s/ECST_ECS' % (archives_dir)
        if not create_directory(ecs_dir):
            return False

    dac_dir = '%s/dac' % (directory)
    if not create_directory(dac_dir):
        return False

    database_dir = '%s/Database' % (directory)
    if not create_directory(database_dir):
        return False

    logging.info(
        'Created the export directory %s successfully ...', directory)
    return True


def export_archives(database_path, environ):
    '''
    '''
    source_path = os.path.join(database_path, 'Archives')
    export_path = os.path.join(environ, 'Archives')

    if environ == 'CMS':
        source_item = os.path.join(source_path, 'POWLIGHT.cfg')
        export_item = os.path.join(
            export_path, 'CMST_POWLIGHT', 'CMST_POWLIGHT.cfg')
        logging.info('Exporting %s to %s ...', source_item, export_item)
        shutil.copy2(source_item, export_item)

        source_item = os.path.join(source_path, 'POWMXD.cfg')
        export_item = os.path.join(
            export_path, 'CMST_POWMXD', 'CMST_POWMXD.cfg')
        logging.info('Exporting %s to %s ...', source_item, export_item)
        shutil.copy2(source_item, export_item)
    elif environ == 'ECS':
        source_item = os.path.join(source_path, 'ECS.cfg')
        export_item = os.path.join(export_path, 'ECST_ECS', 'ECST_ECS.cfg')
        logging.info('Exporting %s to %s ...', source_item, export_item)
        shutil.copy2(source_item, export_item)


def export_dac_files(database_path, environ):
    '''
    '''
    source_path = os.path.join(database_path, 'dac_DB_%s' % (environ))
    export_path = os.path.join(environ, 'dac')

    for item in os.listdir(source_path):
        if item.endswith('.dat'):
            source_item = os.path.join(source_path, item)
            logging.info('Exporting %s to %s ...', source_item, export_path)
            shutil.copy2(source_item, export_path)

    source_item = os.path.join(source_path, environ, 'ScsDacCtrt.cfg')
    logging.info('Exporting %s to %s ...', source_item, export_path)
    shutil.copy2(source_item, export_path)


def export_database_files(database_path, environ):
    '''
    '''
    source_path = os.path.join(database_path, 'Database')
    export_path = os.path.join(environ, 'Database')

    source_item = os.path.join(source_path, 'xml_DB_%s' % (environ))
    export_item = os.path.join(export_path, 'xml')

    if directory_exists(export_item):
        logging.info('Removing the existing %s directory ...', export_item)
        shutil.rmtree(export_item)

    logging.info('Exporting %s to %s ...', source_item, export_item)
    shutil.copytree(source_item, export_item)

    source_item = os.path.join(source_path, 'classlist_%s.txt' % (environ))
    export_item = os.path.join(export_path, 'classlist.txt')

    logging.info('Exporting %s to %s ...', source_item, export_item)
    shutil.copy2(source_item, export_item)


def main():
    '''
    main function
    '''
    init_logging()

    parser = argparse.ArgumentParser(prog='db-prepper')
    parser.add_argument('--database-path', '-d', required=True,
                        dest='database_path', help='path to database directory')
    parser.add_argument('--environment', '-e', nargs='+', required=True,
                        dest='environment', help='name of ISCS environment')

    args = parser.parse_args()

    logging.debug('database_path: %s', args.database_path)

    for environ in args.environment:
        environ = environ.upper()
        logging.debug('environment: %s', environ)

        if not is_environment_valid(environ):
            logging.warn(
                '%s is not a valid ISCS environment name. Skipping ...', environ)
            continue

        if not prerequisites_exists(args.database_path, environ):
            logging.warn(
                '%s does not contain pre-requisites for %s environment; Skipping ...',
                args.database_path, environ)
            continue

        if not create_export_directory(environ):
            logging.warn(
                'Failed to create an export directory for %s environment. Skipping ...',
                environ)
            continue

        export_archives(args.database_path, environ)
        export_dac_files(args.database_path, environ)
        export_database_files(args.database_path, environ)

        logging.info(
            'Prepping database files for %s environment complete ...', environ)


if __name__ == '__main__':
    main()
