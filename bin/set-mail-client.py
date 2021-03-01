#!/usr/bin/env python

import LaunchServices
import argparse

DEFAULT_MAIL_HANDLER = 'com.apple.mail'

def print_mail_handler():
	'''
	Prints the current mail handler's application bundle identifier
	'''
	result = LaunchServices.LSCopyDefaultHandlerForURLScheme('mailto')
	print(result)


def set_mail_handler(identifier=DEFAULT_MAIL_HANDLER):
	'''
	'''
	return LaunchServices.LSSetDefaultHandlerForURLScheme('mailto', identifier)


def main():
	'''
	'''
	parser = argparse.ArgumentParser(prog='set-mail-client',
		description='Sets or prints the default mail client',
		epilog='''
		    You can determine the application bundle identifier of your mail application by running `osascript -e 'id of application "<mail application name>"`
		    ''')

	exclusive_group = parser.add_mutually_exclusive_group()
	exclusive_group.add_argument('--restore-handler', '-r', action='store_true',
		help='restores the default mail handler to Mail (com.apple.Mail)')
	exclusive_group.add_argument('--set-handler', '-s', help='sets the default mail handler')

	args = parser.parse_args()
	print(args)

	handler = None
	if args.restore_handler:
		handler = DEFAULT_MAIL_HANDLER
	elif args.set_handler:
		handler = args.set_handler

	if handler:
		result = set_mail_handler(handler)
		if result == 0:
			print_mail_handler()
		else:
			print('Error: failed to set the mail handler to %s' % handler)
	else:
		print_mail_handler()

if __name__ == '__main__':
	main()
