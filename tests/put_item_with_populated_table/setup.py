import sys


def main(host):
    print "Initializing ..."
    print "Done."


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s host_url" % sys.argv[0]
        sys.exit(-1)
    main(sys.argv[1])