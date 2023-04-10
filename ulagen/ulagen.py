#!/usr/bin/env python

# Original credit: Andrew Ho
# https://github.com/andrewlkho/ulagen

import hashlib
import time
import uuid
import argparse

def get_eui64():
    """
    Retrieve the MAC address of the node running this code.
    Returns the MAC address in canonical format (XX-XX-XX-XX-XX-XX).
    """
    mac = uuid.getnode()
    eui64 = mac >> 24 << 48 | 0xfffe000000 | mac & 0xffffff
    eui64_canon = "-".join([format(eui64, "02X")[i:i+2] for i in range(0, 18, 2)])
    return eui64_canon

def time_ntpformat():
    """
    Return the current NTP-format time.
    """
    # Seconds relative to 1900-01-01 00:00
    return time.time() - time.mktime((1900, 1, 1, 0, 0, 0, 0, 1, -1))

def gen_prefix():
    """
    Generate a prefix in the fd00::/8 address space.
    """
    h = hashlib.sha1()
    h.update((get_eui64() + str(time_ntpformat())).encode('us-ascii'))
    globalid = h.hexdigest()[0:10]

    return ":".join(("fd" + globalid[0:2], globalid[2:6], globalid[6:10]))

# Network suffix masking
mask_suffix = lambda suffix, length : \
        (suffix & ((2**length)-1)) \
        << (64 - length)

def gen_subnet(prefix, suffix, length=64, showlength=True):
    """
    Create a subnet from the given prefix.
    """

    # We only support networks in this size range.
    assert length >= 48, 'Subnet too big'
    assert length <= 64, 'Subnet too small'

    if (suffix == 0) or (length == 48):
        # This is the prefix itself.
        if showlength:
            return '%s::/%s' % (prefix, length)
        else:
            return prefix
    else:
        return '%s:%x::%s' % (
                prefix,
                mask_suffix(suffix, length),
                ('/%d' % length) if showlength else ''
        )

def main(*args):
    parser = argparse.ArgumentParser('IPv6 ULA generator')
    parser.add_argument('--no-length', action='store_const',
            const=True, default=False,
            help='Omit the subnet size in the output')
    parser.add_argument('--subnet', action='append',
            type=str,
            help='Output a subnet with the given 16-bit network suffix.  '\
                 'e.g. 0xcafe or 0xcafe/64 will generate a /64 subnet like '\
                 'fc00:aabb:ccdd:cafe::/64.  Suffix is interpreted as '\
                 'decimal unless 0x prefix is given.  '\
                 'If a variable name followed by \'=\' is given, then '\
                 'the subnet will be prefixed by that same text (for '\
                 'shell scripts), otherwise a name like \'net_XXXX_YY\' '\
                 'where XXXX is the suffix in hex and YY is the length, '\
                 'will be used instead.')

    arguments = parser.parse_args(*args)
    prefix = gen_prefix()

    if not arguments.subnet:
        # Backward compatibility: human readable format
        print ("Prefix:       %s" %\
                gen_subnet(prefix, 0, 48, not arguments.no_length))
        print ("First subnet: %s" %\
                gen_subnet(prefix, 0x0000, 64, not arguments.no_length))
        print ("Last subnet:  %s" %\
                gen_subnet(prefix, 0xffff, 64, not arguments.no_length))
    else:
        # Generate a number of subnets from the prefix.  Shell-parsable output.
        for net_def in arguments.subnet:
            if '=' in net_def:
                (name, net_def) = net_def.split('=',1)
            else:
                name = None

            if '/' in net_def:
                (net_def, length) = net_def.split('/',1)
                length = int(length, 10)
            else:
                length = 64

            suffix = int(net_def, 16 if net_def.startswith('0x') else 10)
            if name is None:
                name = 'net_%04x_%02d' % (suffix, length)

            print ('%s=%s' % (
                name,
                gen_subnet(prefix, suffix, length,
                    not arguments.no_length)))

if __name__ == "__main__":
    main()
