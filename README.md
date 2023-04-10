`ulagen.py` is a short python script to generate an IPv6 unique local address as 
per the pseudo-random algorithm defined in [RFC 
4193](https://tools.ietf.org/html/rfc4193).  Run it without any arguments.  For 
example:

    % ulagen
    Prefix:       fdf3:5237:bf63::/48
    First subnet: fdf3:5237:bf63::/64
    Last subnet:  fdf3:5237:bf63:ffff::/64

It can be called with arguments so you can generate subnet addresses from
within shell scripts and other environments in a format suitable for use
with the shell script `eval` command.  `--subnet` can be specified multiple times.
The format for `--subnet` is:

    [NAME=]SUFFIX[/LEN]

where `NAME` is the name of the variable to output (for use with `eval`),
`SUFFIX` is the suffix to append to the generated prefix, either expressed as
decimal (this will be converted to hexadecimal) or hexadecimal (with a `0x`
prefix), and `LEN` is the optional subnet prefix length in bits (decimal).

By default, `LEN` is assumed to be 64.

`NAME`, if not explicitly defined will default to be `net_XXXX_YY` where `XXXX`
is the subnet suffix expressed in hexadecimal, and `YY` is the subnet prefix
length in decimal.

The `/XX` length can be omitted from the output by giving the `--no-length`
command line argument.

To just spit out the ULA subnet:

    % ulagen --subnet 0/48
    net_0000_48=fdf3:5237:bf63::/48

Omit the `/48` prefix length:

    % ulagen --no-length --subnet 0/48
    net_0000_48=fdf3:5237:bf63::

Custom variable name:

    % ulagen --subnet mynetwork=0
    mynetwork=fdf3:5237:bf63::/64

Multiple subnets:

    % ulagen --subnet dmz=0 --subnet priv1=1 \
             --subnet priv2=2 --subnet priv10=10 --subnet vpns=0x80/56
    dmz=fdf3:5237:bf63::/64
    priv1=fdf3:5237:bf63:1::/64
    priv2=fdf3:5237:bf63:2::/64
    priv10=fdf3:5237:bf63:a::/64
    vpns=fdf3:5237:bf63:8000::/56

You can also import the module into your own scripts, e.g. to re-implement the
original `ulagen.py`:

    import ulagen

    prefix=ulagen.gen_prefix()
    print ('Prefix:       ' + gen_subnet(prefix, 0x0000, 48))
    print ('First subnet: ' + gen_subnet(prefix, 0x0000))
    print ('Last subnet:  ' + gen_subnet(prefix, 0xffff))

For detail, have a look at the `main()` function in `ulagen.py`.
