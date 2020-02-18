#!/usr/bin/env python

import argparse
import logging
import logging.handlers
import os
import os.path
import shutil


def init_logging():
    '''
    Initialize logger
    '''
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    c = logging.StreamHandler()
    c_formatter = logging.Formatter(fmt='%(levelname)s %(message)s')
    c.setFormatter(c_formatter)
    c.setLevel(logging.INFO)

    f = logging.FileHandler('manticore.log')
    f_formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s %(message)s')
    f.setFormatter(f_formatter)
    f.setLevel(logging.INFO)

    logger.addHandler(c)
    logger.addHandler(f)
    return logger


def directory_exists(directory):
    '''
    '''
    logging.info('Checking if %s exists...', directory)
    if os.path.isdir(directory):
        logging.info('OK')
        return True

    logging.error('%s does not exist', directory)
    return False


def create_directory(directory):
    '''
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
    '''
    logging.info('Checking if %s exists...', infile)
    if os.path.isfile(infile):
        logging.info('OK')
        return True

    logging.error('%s does not exist', infile)
    return False


def prerequisites_exists(database_path, environment):
    '''
    '''
    archives_dir = '%s/Archives/DB_%s' % (database_path, environment)
    if not directory_exists(archives_dir):
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

    return True


def create_export_directory(directory):
    '''
    '''
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

    return True


def main():
    '''
    main function
    '''
    init_logging()

    parser = argparse.ArgumentParser(prog='db-prepper')
    parser.add_argument('--database-path', '-d', required=True,
                        dest='database_path', help='path to database directory')
    parser.add_argument('--environment', '-e', required=True,
                        dest='environment', help='name of ISCS environment')

    args = parser.parse_args()
    logging.info('args: %s', args)

    '''
    Check if all required files and directories exist.
    Each database package should have the following:
    - Archives/DB_xxx
    - dac_DB_xxx
    - dac_DB_xxx/xxx/ScsDacCtrt.cfg
    - Database/xml_DB_xxx
    - Database/classlist_xxx.txt

    We should be able to find these under the database_path.
    '''
    result = prerequisites_exists(args.database_path, args.environment)
    if not result:
        exit(1)

    '''
    Create a template directory for the environment
    Each environment database package should have the following directory:
    - xxx/Archives
    - xxx/dac
    - xxx/Database
    '''
    result = create_export_directory(args.environment)
    if not result:
        exit(1)

    '''
    Copy the following files and directories:
    - Archives/DB_xxx (this will be handled later)
    - dac_DB_xxx/*.dat to dac/*.dat
    - dac_DB_xxx/xxx/ScsDacCtrt.cfg to dac/ScsDacCtrt.cfg
    - Database/xml_DB_xxx to Database/xml
    - Database/classlist_xxx.txt to Database/classlist.txt
    '''

    '''
    CMS
    - Archives/CMST_POWLIGHT/CMST_POWLIGHT.cfg
    - Archives/CMST_POWMXD/CMST_POWMXD.cfg

    ECS
    - Archives/ECST_ECS/ECST_ECS.cfg

    ATS
    - Archives is empty

    DBS
    - There are no DB package for DBS

    EMS
    - Archives is empty

    NED
    - Archives is empty
    '''

    source_path = '%s/Archives' % (args.database_path)
    dest_path = '%s/Archives' % (args.environment)

    # For now, assume that only CMS and ECS have the Archives with meaningful data
    if args.environment == 'CMS':
        logging.info('Copying Archives configuration files for CMS ...')
        '''
        Archives/POWLIGHT.cfg -> Archives/CMST_POWLIGHT/CMST_POWLIGHT.cfg
        Archives/POWMXD.cfg -> Archives/CMST_POWMXD/CMST_POWMXD.cfg
        '''
        source_item = '%s/POWLIGHT.cfg' % (source_path)
        dest_item = '%s/CMST_POWLIGHT/CMST_POWLIGHT.cfg' % (dest_path)
        shutil.copy2(source_item, dest_item)

        source_item = '%s/POWMXD.cfg' % (source_path)
        dest_item = '%s/CMST_POWMXD/CMST_POWMXD.cfg' % (dest_path)
        shutil.copy2(source_item, dest_item)

    elif args.environment == 'ECS':
        logging.info('Copying Archives configuration files for ECS ...')
        '''
        Archives/ECS.cfg -> Archives/ECST_ECS/ECST_ECS.cfg
        '''
        source_item = '%s/ECS.cfg' % (source_path)
        dest_item = '%s/ECST_ECS/ECST_ECS.cfg' % (dest_path)
        shutil.copy2(source_item, dest_item)

    source_path = '%s/dac_DB_%s/' % (args.database_path, args.environment)
    dest_path = '%s/dac' % (args.environment)

    logging.info('Copying *.dat files from %s to %s ...',
                 source_path, dest_path)
    for item in os.listdir(source_path):
        if item.endswith('.dat'):
            source_file = '%s/%s' % (source_path, item)
            shutil.copy2(source_file, dest_path)

    source_item = '%s/%s/ScsDacCtrt.cfg' % (source_path, args.environment)
    logging.info('Copying ScsDacCtrt.cfg from %s to %s ...',
                 source_path, dest_path)
    shutil.copy2(source_item, dest_path)

    source_path = '%s/Database' % (args.database_path)
    dest_path = '%s/Database' % (args.environment)

    # Copy database xml_DB_xxx

    source_item = '%s/xml_DB_%s' % (source_path, args.environment)
    dest_item = '%s/xml' % (dest_path)

    logging.info('Copying %s to %s ...', source_item, dest_item)
    shutil.copytree(source_item, dest_item)

    # Copy database classlist_xxx.txt

    source_item = '%s/classlist_%s.txt' % (source_path, args.environment)
    dest_item = '%s/classlist.txt' % (dest_path)
    logging.info('Copying classlist_%s.txt to %s ...',
                 args.environment, dest_item)
    shutil.copy2(source_item, dest_item)


if __name__ == '__main__':
    main()
