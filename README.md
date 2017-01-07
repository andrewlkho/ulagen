`ulagen.py` is a short python script to generate an IPv6 unique local address as 
per the pseudo-random algorithm defined in [RFC 
4193](https://tools.ietf.org/html/rfc4193).  Run it without any arguments.  For 
example:

    % ./ulagen.py
    Prefix:       fdf3:5237:bf63::/48
    First subnet: fdf3:5237:bf63::/64
    Last subnet:  fdf3:5237:bf63:ffff::/64
