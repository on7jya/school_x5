import sys
import time

from moex import *

WAIT_TIME = 60  # default refresh time


def main():
    logger = log_to_file(namelogger="moex_X5")
    logger.info("============================")
    logger.info("Started...")
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    refresh_time = None
    logger.info('args.format = ' + args.format)
    logger.info('args.out = ' + args.out)
    logger.info('args.watch = ' + str(args.watch))
    logger.info('args.refresh = ' + str(refresh_time))

    if args.watch:
        logger.info("watch turned on")
        if isinstance(args.refresh, int):
            refresh_time = args.refresh
        else:
            refresh_time = WAIT_TIME
        while True:
            try:
                response_xml = get_request_moex()
                updated_file = parse_xml(response_xml, args.format, args.out)
                if updated_file:
                    log_to_console('Data has been updated')
                else:
                    log_to_console('No updates')
                time.sleep(refresh_time)
            except KeyboardInterrupt:
                logger.debug('User aborted operation')
                exit()
    else:
        response_xml = get_request_moex()
        parse_xml(response_xml, args.format, args.out)
    logger.info("Successful!")


if __name__ == "__main__":
    main()

# python kotirovki.py -format csv -out ./output_task_3.csv
# python kotirovki.py -format json -out ./output_task_3.json
# python kotirovki.py -format xml -out ./output_task_3.xml
