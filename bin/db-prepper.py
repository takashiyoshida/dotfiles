#!/usr/bin/env python3

import argparse
import logging
import logging.handlers
import os
import os.path
import shutil
import tarfile

# A list of valid environment
# NUP is specific to NELNUP project and does not exist in other projects (i.e. C755B)
ENVIRONMENT = ['ATS', 'BGK', 'BNK', 'CMS', 'CNT', 'CQY', 'DBG', 'ECS', 'EMS', 'FRP', 'HBF',
               'HGN', 'KVN', 'LTI', 'NED', 'NMS', 'OTP', 'PGC', 'PGL', 'PTP', 'SER', 'SKG', 'WLH']

WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'


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
    f.setLevel(logging.DEBUG)

    logger.addHandler(c)
    logger.addHandler(f)
    return logger


def is_environment_valid(environment):
    '''
    Returns true if the given environment name is valid.
    See ENVIRONMENT for the valid environment name
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


def search_and_replace(infile, search, replace):
    '''
    '''
    text = open(infile, 'rb').read().replace(bytes(search, 'utf-8'), bytes(replace, 'utf-8'))
    open(infile, 'wb').write(text)


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

    archives_dir = os.path.join(
        database_path, 'Archives', 'DB_%s' % (environment))

    if not directory_exists(archives_dir):
        return False

    if environment == 'CMS':
        powlight_cfg = os.path.join(archives_dir, 'POWLIGHT.cfg')
        if not file_exists(powlight_cfg):
            return False

        powmxd_cfg = os.path.join(archives_dir, 'POWMXD.cfg')
        if not file_exists(powmxd_cfg):
            return False
    elif environment == 'ECS':
        ecs_cfg = os.path.join(archives_dir, 'ECS.cfg')
        if not file_exists(ecs_cfg):
            return False

    dac_dir = os.path.join(database_path, 'dac_DB_%s' % (environment))
    if not directory_exists(dac_dir):
        return False

    concentrator = os.path.join(database_path, 'dac_DB_%s' % (
        environment), environment, 'ScsDacCtrt.cfg')
    if not file_exists(concentrator):
        return False

    xml_dir = os.path.join(database_path, 'Database',
                           'xml_DB_%s' % (environment))
    if not directory_exists(xml_dir):
        return False

    classlist = os.path.join(database_path, 'Database',
                             'classlist_%s.txt' % (environment))
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
        powlight_dir = os.path.join(archives_dir, 'CMST_POWLIGHT')
        if not create_directory(powlight_dir):
            return False

        powmxd_dir = os.path.join(archives_dir, 'CMST_POWMXD')
        if not create_directory(powmxd_dir):
            return False

    elif directory == 'ECS':
        ecs_dir = os.path.join(archives_dir, 'ECST_ECS')
        if not create_directory(ecs_dir):
            return False

    dac_dir = os.path.join(directory, 'dac')
    if not create_directory(dac_dir):
        return False

    database_dir = os.path.join(directory, 'Database')
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
        search_and_replace(export_item, 'POWLIGHT', 'CMST_POWLIGHT')

        source_item = os.path.join(source_path, 'POWMXD.cfg')
        export_item = os.path.join(
            export_path, 'CMST_POWMXD', 'CMST_POWMXD.cfg')
            
        logging.info('Exporting %s to %s ...', source_item, export_item)
        shutil.copy2(source_item, export_item)
        search_and_replace(export_item, 'POWMXD', 'CMST_POWMXD')
    elif environ == 'ECS':
        source_item = os.path.join(source_path, 'ECS.cfg')
        export_item = os.path.join(export_path, 'ECST_ECS', 'ECST_ECS.cfg')

        logging.info('Exporting %s to %s ...', source_item, export_item)
        shutil.copy2(source_item, export_item)
        search_and_replace(export_item, 'ECS.cfg', 'ECST_ECS.cfg')
        search_and_replace(export_item, '"ECS"', '"ECST_ECS"')


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


def fix_file_line_ending(file_path):
    with open(file_path, 'rb') as infile:
        content = infile.read()

    content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
    with open(file_path, 'wb') as outfile:
        outfile.write(content)

def main():
    '''
    main function
    '''
    init_logging()

    parser = argparse.ArgumentParser(prog='db-prepper', description='Generate a tarball from Configurator\'s output.')
    # Path to database directory
    parser.add_argument('--database-path', '-d', required=True,
                        dest='database_path', help='path to database directory')
    # Enter the environment name (i.e. CMS, ATS, HBF, ..., PGL)
    # Lowercase environment names are converted to uppercase environment names automatically.
    parser.add_argument('--environment', '-e', nargs='+', required=False, default='',
                        dest='environment', help='name of ISCS environment')
    parser.add_argument('--compress', '-z', required=False, dest='db_version',
                        help='creates a tarball from exported files')
    parser.add_argument('--fix-line-ending', '-f', action='store_true', required=False, 
                        dest='fix_line_ending', help='fix Windows line-ending')

    args = parser.parse_args()

    logging.debug('database_path: %s', args.database_path)
    if args.db_version == None:
        logging.debug('db_version was not specified')
    else:
        logging.debug('db_version: %s', args.db_version)

    if args.environment == '':
        args.environment = ENVIRONMENT

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


    if args.db_version != None:
        for environ in args.environment:
            if directory_exists(environ):
                outfile = 'NELDB_%s_C755B_%s.tar.gz' % (
                    environ, args.db_version)
                logging.info(
                    'Creating a tarball %s from %s directory ...', outfile, environ)
                with tarfile.open(outfile, 'w:gz') as tar:
                    tar.add(environ, arcname=os.path.basename(environ))
                logging.info('OK')
            else:
                logging.warn('%s does not exist. Skipping ...', environ)

    if args.fix_line_ending:
        for environ in args.environment:
            # dbmuserconst_class_*.cfg files are at args.database_path
            class_cfg = os.path.join(args.database_path, 'Database', 
                                     'dbmuserconst_class_%s.cfg' % (environ))
            classlist = os.path.join(args.database_path, 'Database', 
                                     'classlist_%s.txt' % (environ))
            if file_exists(class_cfg):
                logging.info('Converting Windows line ending to UNIX line ending in %s...', class_cfg)
                fix_file_line_ending(class_cfg)

            if file_exists(classlist):
                logging.info('Converting Windows line ending to UNIX line ending in %s...', class_cfg)
                fix_file_line_ending(classlist)


if __name__ == '__main__':
    main()
